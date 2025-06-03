# 🎙️ Advanced Voice Converter Pro

A comprehensive Text-to-Speech (TTS) and Speech-to-Text (STT) application built with Python, featuring a modern GUI and advanced functionality for voice conversion tasks.

## 🌟 Features

### Text-to-Speech (TTS)
- **Multi-voice Support**: Choose from available system voices
- **Customizable Settings**: Adjust speech rate, volume, and voice selection
- **Quick Phrases**: Pre-built common phrases for quick access
- **Audio Export**: Save speech as MP3/WAV files using Google TTS
- **Real-time Controls**: Start, stop, and clear functionality

### Speech-to-Text (STT)
- **Live Recording**: Real-time speech recognition from microphone
- **Audio File Processing**: Upload and process existing audio files
- **Multiple Format Support**: WAV, MP3, FLAC, M4A files
- **Timestamped Output**: Automatic timestamping of recognized speech
- **Google Speech Recognition**: High-accuracy speech recognition

### Advanced Features
- **History Management**: Complete conversation history with timestamps
- **Settings Persistence**: Saves your preferences between sessions
- **Export Functionality**: Export history as JSON or text files
- **Microphone Testing**: Built-in microphone functionality test
- **Cross-platform Compatibility**: Works on Windows, macOS, and Linux
- **Modern UI**: Tabbed interface with intuitive controls
- **Error Handling**: Comprehensive error handling and user feedback

## 🚀 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/harshit001-2023/voice-converter-pro.git
   cd voice-converter-pro
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Additional Setup (Windows)**
   - For PyAudio on Windows, you might need to install it separately:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

4. **Run the Application**
   ```bash
   python voice_converter.py
   ```

## 🛠️ Dependencies

- **pyttsx3**: Cross-platform text-to-speech library
- **SpeechRecognition**: Library for performing speech recognition
- **gTTS**: Google Text-to-Speech API wrapper
- **pygame**: For audio playback functionality
- **pyaudio**: For microphone input handling
- **tkinter**: GUI framework (usually comes with Python)

## 📱 Usage

### Getting Started
1. Launch the application by running `python voice_converter.py`
2. The application opens with four main tabs: TTS, STT, Settings, and History

### Text-to-Speech
1. Navigate to the "🔊 Text to Speech" tab
2. Enter your text in the input field
3. Click "🎤 Speak" to hear the text
4. Use quick phrases for common expressions
5. Save audio files using "💾 Save Audio"

### Speech-to-Text
1. Go to the "🎙️ Speech to Text" tab
2. Click "🎙️ Start Recording" and speak clearly
3. Or upload an existing audio file with "📁 Upload Audio"
4. View results in the output area
5. Copy recognized text to TTS with "📋 Copy to TTS"

### Settings Configuration
1. Access the "⚙️ Settings" tab to customize:
   - Speech rate (50-300 words per minute)
   - Volume level (0.1-1.0)
   - Voice selection from available system voices
   - Microphone testing

### History Management
1. Check the "📝 History" tab for all activities
2. Export your history as JSON or text files
3. Clear history when needed

## 🎯 Key Features Showcase

### 🔧 Technical Features
- **Multithreading**: Non-blocking UI during speech operations
- **Configuration Management**: JSON-based settings persistence
- **Error Handling**: Comprehensive exception handling
- **File I/O Operations**: Audio and text file processing
- **Cross-platform Audio**: Works on multiple operating systems

### 🎨 User Experience
- **Intuitive Interface**: Clean, tabbed design
- **Real-time Feedback**: Status updates and progress indicators
- **Accessibility**: Large buttons and clear text
- **Customization**: Adjustable voice parameters
- **Data Persistence**: Saves settings and history

## 🏗️ Architecture

```
voice_converter.py
├── VoiceConverterApp (Main Class)
├── UI Components
│   ├── TTS Tab (Text-to-Speech Interface)
│   ├── STT Tab (Speech-to-Text Interface)
│   ├── Settings Tab (Configuration)
│   └── History Tab (Activity Log)
├── Core Functions
│   ├── TTS Engine (pyttsx3)
│   ├── STT Recognition (SpeechRecognition)
│   ├── Audio Processing (pygame, pyaudio)
│   └── File Management (JSON, Audio files)
└── Data Management
    ├── Configuration (voice_config.json)
    └── History (voice_history.json)
```

## 🔍 Code Highlights

### Advanced Python Concepts Demonstrated
- **Object-Oriented Programming**: Clean class structure with encapsulation
- **Threading**: Asynchronous operations for responsive UI
- **File Handling**: JSON configuration and audio file processing
- **Exception Handling**: Robust error management
- **GUI Development**: Tkinter with modern design principles
- **API Integration**: Google Text-to-Speech and Speech Recognition

### Key Functions
- `speak_text()`: TTS with threading and error handling
- `start_recording()`: Real-time speech recognition
- `save_audio()`: Export TTS to audio files
- `load_config()` / `save_config()`: Settings management
- `add_to_history()`: Activity logging with timestamps

## 🚀 Future Enhancements

- [ ] Multiple language support
- [ ] Voice cloning integration
- [ ] Real-time voice effects
- [ ] Cloud storage integration
- [ ] Batch file processing
- [ ] Voice command execution
- [ ] Audio visualization
- [ ] Plugin system for extensions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- **pyttsx3** for cross-platform TTS functionality
- **SpeechRecognition** for speech-to-text capabilities
- **Google Cloud Speech-to-Text** for accurate recognition
- **Python community** for excellent libraries and documentation

## 📧 Contact

Harshit Pande- harshitpande938@gmail.com
Project Link: [https://github.com/harshit001-2023/voice-converter-pro](https://github.com/harshit001-2023/voice-converter-pro)

---

⭐ **Star this repository if you found it helpful!** ⭐
   
