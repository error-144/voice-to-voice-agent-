import json
import logging
import sounddevice as sd
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    metrics,
    RoomInputOptions,
)
from livekit.agents.voice import MetricsCollectedEvent

from livekit.plugins import (
    openai,
    speechmatics,
    silero,
    murf,
)

from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins.speechmatics.stt import OperatingPoint




load_dotenv()
logger = logging.getLogger("voice-agent")





sd.default.device = (0, None)  # microphone input


# ───────────────────────────────────────────────────────────────
#  MAIN AGENT CLASS
# ───────────────────────────────────────────────────────────────

class Assistant(Agent):
    def __init__(self, context: dict = None) -> None:
        # Build instructions based on context
        base_instructions = (
            "You are a professional interview assistant conducting a voice interview. "
            "Your interface with users will be voice. "
            "You should use short and concise responses, avoiding usage of unpronounceable punctuation. "
        )
        
        super().__init__(
            instructions=base_instructions,

            # SPEECHMATICS REALTIME STT
            stt=speechmatics.STT(
                language="en",
                operating_point=OperatingPoint.ENHANCED,
                enable_partials=True,
                max_delay=0.7,
                end_of_utterance_silence_trigger=0.5,
                enable_diarization=True,
                speaker_active_format="<speaker_{speaker_id}>{text}</speaker_{speaker_id}>",
                speaker_passive_format="{text}",
                
            ),

            # OPENAI LLM
            llm=openai.LLM(
                model="gpt-4o-mini"
            ),

            # MURF AI TTS
            tts=murf.TTS(
                voice="Matthew",
                style="Conversation",
            ),

            # TURN DETECTION
            turn_detection=MultilingualModel(),
        )

    # Called when agent joins the room
    async def on_enter(self):
        """Called when the agent enters the session."""
        greeting = "Hello! I'm ready to start the interview. How are you doing today?"
        await self.session.generate_reply(
            instructions=greeting,
            allow_interruptions=True,
        )


# ───────────────────────────────────────────────────────────────
#  PREWARM PROCESS
# ───────────────────────────────────────────────────────────────

def prewarm(proc: JobProcess):
    """Load models before agent starts."""
    proc.userdata["vad"] = silero.VAD.load()


# ───────────────────────────────────────────────────────────────
#  MAIN ENTRYPOINT
# ───────────────────────────────────────────────────────────────

async def entrypoint(ctx: JobContext):
    """Main entrypoint for the agent job."""
    try:
        logger.info(f"connecting to room {ctx.room.name}")
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

        # Wait for the first participant to connect
        participant = await ctx.wait_for_participant()
        logger.info(f"starting voice assistant for participant {participant.identity}")
    except Exception as e:
        logger.error(f"Error during entrypoint setup: {e}", exc_info=True)
        raise

    # Extract context from room metadata
    context = None
    try:
        if ctx.room.metadata:
            context = json.loads(ctx.room.metadata)
            logger.info(f"Loaded context from room metadata: {context}")
    except Exception as e:
        logger.warning(f"Could not parse room metadata: {e}")

    # Usage metrics
    usage_collector = metrics.UsageCollector()

    # Agent session
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        # minimum delay for endpointing, used when turn detector believes the user is speaking
        min_endpointing_delay=0.5,
        # maximum delay for endpointing, used when turn detector does not believe the user is done
        max_endpointing_delay=5.0,
    )
             
    @session.on("metrics_collected")
    def on_metrics_collected(ev: MetricsCollectedEvent):
        """Handle metrics collection events."""
        try:
            metrics.log_metrics(ev.metrics)
            usage_collector.collect(ev.metrics)
        except Exception as e:
            logger.warning(f"Error collecting metrics: {e}", exc_info=True)

    # Configure room input options
    room_input_opts = RoomInputOptions()
    
    
    await session.start(
        room=ctx.room,
        agent=Assistant(context=context),
        room_input_options=room_input_opts,
    )


# ───────────────────────────────────────────────────────────────
#  START APPLICATION
# ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        )
    )
