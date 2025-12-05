# 🎤 Voice-to-Voice Interview Agent

A sophisticated real-time voice interview assistant built with the LiveKit Agents framework. This agent conducts natural, conversational interviews using state-of-the-art speech recognition, language understanding, and text-to-speech technologies.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎯 **Real-time Voice Conversations** - Seamless, low-latency voice interactions
- 🗣️ **Speaker Diarization** - Automatically identifies and labels different speakers
- 🧠 **Intelligent Responses** - Powered by OpenAI's GPT-4o-mini for natural conversations
- 🔊 **Natural Voice Synthesis** - High-quality TTS using Murf AI with conversational style
- 🎙️ **Voice Activity Detection** - Silero VAD for accurate speech detection
- 🔄 **Turn Detection** - Multilingual model for natural conversation flow
- 📊 **Usage Metrics** - Built-in metrics collection for monitoring and analytics
- ⚙️ **Context-Aware** - Supports custom interview context via room metadata

## 🏗️ Architecture

This agent leverages a modern pipeline of AI services:

```
User Voice → Speechmatics STT → OpenAI LLM → Murf AI TTS → Agent Voice
                ↓
         Speaker Diarization
                ↓
         Turn Detection & VAD
```

### Technology Stack

- **Speech-to-Text**: [Speechmatics](https://www.speechmatics.com/) - Real-time transcription with enhanced operating point
- **Language Model**: [OpenAI GPT-4o-mini](https://openai.com/) - Fast and efficient conversational AI
- **Text-to-Speech**: [Murf AI](https://murf.ai/) - Natural voice synthesis (Matthew voice, Conversation style)
- **Voice Activity Detection**: [Silero VAD](https://github.com/snakers4/silero-vad) - Accurate speech detection
- **Turn Detection**: Multilingual Model - Intelligent conversation turn management
- **Framework**: [LiveKit Agents](https://docs.livekit.io/agents/) - Real-time communication infrastructure

## 📋 Prerequisites

- Python 3.8 or higher
- API keys for:
  - Speechmatics
  - OpenAI
  - Murf AI
  - LiveKit (for production deployment)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd voice-to-voice-agent-
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# LiveKit Configuration
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Speechmatics API
SPEECHMATICS_API_KEY=your-speechmatics-key

# OpenAI API
OPENAI_API_KEY=your-openai-key

# Murf AI API
MURF_API_KEY=your-murf-key
```

### 4. Run the Agent

**Development Mode (Console):**
```bash
python agent.py dev
```

**Production Mode:**
```bash
python agent.py start
```

## 📖 Usage

### Basic Interview

The agent will automatically greet participants and conduct an interview. The agent is configured to:
- Use short, concise responses
- Avoid unpronounceable punctuation
- Maintain a professional interview tone

### Custom Context (Optional)

You can provide interview context via LiveKit room metadata (JSON format):

```json
{
  "job_position": "Software Engineer",
  "job_description": "We are looking for a full-stack developer...",
  "interview_duration": 30
}
```

The agent will use this context to customize the interview experience.

## 🔧 Configuration

### Speech-to-Text Settings

The agent uses Speechmatics with the following configuration:
- **Language**: English (`en`)
- **Operating Point**: Enhanced (higher accuracy)
- **Max Delay**: 0.7 seconds
- **End of Utterance**: 0.5 seconds silence trigger
- **Diarization**: Enabled (identifies different speakers)

### Language Model

- **Model**: `gpt-4o-mini` (fast and cost-effective)
- Can be changed in `agent.py` line 78

### Text-to-Speech

- **Voice**: Matthew (Murf AI)
- **Style**: Conversation
- Can be customized in `agent.py` lines 82-85

### Endpointing Delays

- **Minimum**: 0.5 seconds (when turn detector confirms user is done)
- **Maximum**: 5.0 seconds (when turn detector is uncertain)

## 📁 Project Structure

```
voice-to-voice-agent-/
├── agent.py              # Main agent implementation
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── LICENSE              # License file
```

## 🧪 Development

### Running in Console Mode

For local testing and development:

```bash
python agent.py dev
```

### Logging

The agent uses Python's logging module. Logs are output to the console with INFO level by default.

### Metrics

Usage metrics are automatically collected and logged. You can access them via the `MetricsCollectedEvent` handler in the code.

## 🔍 Troubleshooting

### Common Issues

1. **Microphone not detected**
   - Check line 42 in `agent.py` - you may need to adjust the sound device index
   - On macOS/Linux, list devices: `python -c "import sounddevice; print(sounddevice.query_devices())"`

2. **API Key Errors**
   - Ensure all required API keys are set in your `.env` file
   - Verify keys are valid and have sufficient credits/quota

3. **Connection Issues**
   - Check your LiveKit server URL and credentials
   - Ensure network connectivity to LiveKit server

4. **Model Loading Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you have sufficient disk space for model downloads

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 🙏 Acknowledgments

- [LiveKit](https://livekit.io/) for the excellent agents framework
- [Speechmatics](https://www.speechmatics.com/) for real-time transcription
- [OpenAI](https://openai.com/) for language model capabilities
- [Murf AI](https://murf.ai/) for natural voice synthesis
- [Silero](https://github.com/snakers4/silero-vad) for voice activity detection

## 📧 Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Built with ❤️ using LiveKit Agents**
