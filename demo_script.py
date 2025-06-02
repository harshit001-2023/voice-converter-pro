#!/usr/bin/env python3
"""
Demo script for Voice Converter Pro
This script demonstrates the core functionality without GUI
"""

import pyttsx3
import speech_recognition as sr
import time
from gtts import gTTS
import os
import tempfile
import pygame

def demo_text_to_speech():
    """Demonstrate Text-to-Speech functionality"""
    print("=" * 50)
    print("🔊 TEXT-TO-SPEECH DEMO")
    print("=" * 50)
    
    # Initialize TTS engine
    engine = pyttsx3.init()
    
    # Get available voices
    voices = engine.getProperty('voices')
    print(f"Available voices: {len(voices)}")
    for i, voice in enumerate(voices[:3]):  # Show first 3 voices
        print(f"  {i+1}. {voice.name if hasattr(voice, 'name') else f'Voice {i+1}'}")
    
    # Demo text
    demo_text = "Hello! Welcome to Voice Converter Pro. This is a demonstration of text-to-speech functionality."
    
    print(f"\nSpeaking: '{demo_text}'")
    print("🎤 Playing audio...")
    
    # Configure and speak
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.9)
    engine.say(demo_text)
    engine.runAndWait()
    
    print("✅ Text-to-Speech demo completed!")

def demo_speech_to_text():
    """Demonstrate Speech-to-Text functionality"""
    print("\n" + "=" * 50)
    print("🎙️ SPEECH-TO-TEXT DEMO")
    print("=" * 50)
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print("🎤 Microphone test...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    print("✅ Microphone ready!")
    
    print("\n🔴 Recording in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("🎙️ Speak now! (You have 5 seconds)")
    
    try:
        with microphone as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        print("🔄 Processing speech...")
        text = recognizer.recognize_google(audio)
        
        print(f"✅ Recognized: '{text}'")
        
        # Convert recognized text back to speech
        print("🔄 Converting back to speech...")
        engine = pyttsx3.init()
        engine.say(f"You said: {text}")
        engine.runAndWait()
        
    except sr.WaitTimeoutError:
        print("❌ No speech detected within timeout period")
    except sr.UnknownValueError:
        print("❌ Could not understand the speech")
    except sr.RequestError as e:
        print(f"❌ Speech recognition error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_google_tts():
    """Demonstrate Google TTS with file saving"""
    print("\n" + "=" * 50)
    print("🌐 GOOGLE TTS DEMO")
    print("=" * 50)
    
    text = "This is a demonstration of Google Text-to-Speech with file saving capability."
    
    try:
        print(f"Converting: '{text}'")
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_filename = temp_file.name
            tts.save(temp_filename)
        
        print(f"✅ Audio saved to: {temp_filename}")
        
        # Play the saved audio
        print("🎵 Playing saved audio...")
        pygame.mixer.init()
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        
        # Wait for playback to complete
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        # Clean up
        os.unlink(temp_filename)
        print("✅ Google TTS demo completed!")
        
    except Exception as e:
        print(f"❌ Google TTS error: {e}")

def demo_features():
    """Demonstrate key features"""
    print("\n" + "=" * 50)
    print("⚡ FEATURE SHOWCASE")
    print("=" * 50)
    
    features = [
        "✅ Cross-platform compatibility",
        "✅ Multiple TTS engines (pyttsx3 + Google TTS)",
        "✅ Real-time speech recognition",
        "✅ Audio file processing",
        "✅ Customizable voice settings",
        "✅ History management",
        "✅ Export functionality",
        "✅ Modern GUI interface",
        "✅ Error handling",
        "✅ Configuration persistence"
    ]
    
    print("🚀 Voice Converter Pro Features:")
    for feature in features:
        print(f"   {feature}")
        time.sleep(0.2)

def main():
    """Main demo function"""
    print("🎯 VOICE CONVERTER PRO - DEMO")
    print("A comprehensive TTS & STT application")
    print("Showcasing Python skills for your portfolio!")
    
    try:
        # Feature showcase
        demo_features()
        
        # TTS Demo
        demo_text_to_speech()
        
        # Google TTS Demo
        demo_google_tts()
        
        # STT Demo (optional - requires microphone)
        response = input("\n🎙️ Do you want to test Speech-to-Text? (y/n): ").lower().strip()
        if response == 'y':
            demo_speech_to_text()
        else:
            print("⏭️ Skipping Speech-to-Text demo")
        
        print("\n" + "=" * 50)
        print("🎉 DEMO COMPLETED!")
        print("=" * 50)
        print("To run the full application with GUI:")
        print("python voice_converter.py")
        print("\nRepository: https://github.com/yourusername/voice-converter-pro")
        
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
