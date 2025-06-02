import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import pyttsx3
import speech_recognition as sr
import threading
import json
import os
from datetime import datetime
import pygame
import io
from gtts import gTTS
import tempfile
import wave
import pyaudio

class VoiceConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Voice Converter Pro")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Initialize components
        self.tts_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
        # Configuration
        self.config_file = "voice_config.json"
        self.history_file = "voice_history.json"
        self.load_config()
        self.load_history()
        
        # Variables
        self.is_recording = False
        self.is_speaking = False
        
        self.setup_ui()
        self.setup_tts_settings()
        
    def load_config(self):
        """Load saved configuration"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                'voice_rate': 200,
                'voice_volume': 0.9,
                'voice_id': 0,
                'theme': 'dark'
            }
    
    def save_config(self):
        """Save current configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)
    
    def load_history(self):
        """Load conversation history"""
        try:
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []
    
    def save_history(self):
        """Save conversation history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # TTS Tab
        self.create_tts_tab()
        
        # STT Tab
        self.create_stt_tab()
        
        # Settings Tab
        self.create_settings_tab()
        
        # History Tab
        self.create_history_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W, bg='#34495e', fg='white')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_tts_tab(self):
        """Create Text-to-Speech tab"""
        tts_frame = ttk.Frame(self.notebook)
        self.notebook.add(tts_frame, text='🔊 Text to Speech')
        
        # Input section
        input_label = tk.Label(tts_frame, text="Enter text to convert to speech:", 
                              font=('Arial', 12, 'bold'), bg='#ecf0f1')
        input_label.pack(pady=10)
        
        self.tts_text = scrolledtext.ScrolledText(tts_frame, height=8, width=80,
                                                 font=('Arial', 11))
        self.tts_text.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Button frame
        button_frame = tk.Frame(tts_frame, bg='#ecf0f1')
        button_frame.pack(pady=10)
        
        # Speak button
        self.speak_btn = tk.Button(button_frame, text="🎤 Speak", 
                                  command=self.speak_text, bg='#3498db', fg='white',
                                  font=('Arial', 12, 'bold'), padx=20)
        self.speak_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_btn = tk.Button(button_frame, text="⏹️ Stop", 
                                 command=self.stop_speaking, bg='#e74c3c', fg='white',
                                 font=('Arial', 12, 'bold'), padx=20)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Save audio button
        save_audio_btn = tk.Button(button_frame, text="💾 Save Audio", 
                                  command=self.save_audio, bg='#2ecc71', fg='white',
                                  font=('Arial', 12, 'bold'), padx=20)
        save_audio_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = tk.Button(button_frame, text="🗑️ Clear", 
                             command=lambda: self.tts_text.delete(1.0, tk.END),
                             bg='#95a5a6', fg='white', font=('Arial', 12, 'bold'), padx=20)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Quick phrases
        phrases_frame = tk.LabelFrame(tts_frame, text="Quick Phrases", 
                                     font=('Arial', 10, 'bold'), bg='#ecf0f1')
        phrases_frame.pack(pady=10, padx=20, fill='x')
        
        phrases = ["Hello, how are you?", "Thank you very much!", 
                  "Have a great day!", "Good morning!", "Goodbye!"]
        
        for i, phrase in enumerate(phrases):
            btn = tk.Button(phrases_frame, text=phrase, 
                           command=lambda p=phrase: self.insert_phrase(p),
                           bg='#f39c12', fg='white', font=('Arial', 9))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_stt_tab(self):
        """Create Speech-to-Text tab"""
        stt_frame = ttk.Frame(self.notebook)
        self.notebook.add(stt_frame, text='🎙️ Speech to Text')
        
        # Control section
        control_frame = tk.Frame(stt_frame, bg='#ecf0f1')
        control_frame.pack(pady=20)
        
        # Record button
        self.record_btn = tk.Button(control_frame, text="🎙️ Start Recording", 
                                   command=self.toggle_recording, bg='#e74c3c', fg='white',
                                   font=('Arial', 14, 'bold'), padx=30, pady=10)
        self.record_btn.pack(side=tk.LEFT, padx=10)
        
        # Upload audio button
        upload_btn = tk.Button(control_frame, text="📁 Upload Audio", 
                              command=self.upload_audio, bg='#9b59b6', fg='white',
                              font=('Arial', 12, 'bold'), padx=20)
        upload_btn.pack(side=tk.LEFT, padx=10)
        
        # Output section
        output_label = tk.Label(stt_frame, text="Recognized Speech:", 
                               font=('Arial', 12, 'bold'), bg='#ecf0f1')
        output_label.pack(pady=(20, 10))
        
        self.stt_output = scrolledtext.ScrolledText(stt_frame, height=10, width=80,
                                                   font=('Arial', 11))
        self.stt_output.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Action buttons
        action_frame = tk.Frame(stt_frame, bg='#ecf0f1')
        action_frame.pack(pady=10)
        
        # Copy to TTS button
        copy_btn = tk.Button(action_frame, text="📋 Copy to TTS", 
                            command=self.copy_to_tts, bg='#3498db', fg='white',
                            font=('Arial', 11, 'bold'), padx=15)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Save text button
        save_text_btn = tk.Button(action_frame, text="💾 Save Text", 
                                 command=self.save_text, bg='#2ecc71', fg='white',
                                 font=('Arial', 11, 'bold'), padx=15)
        save_text_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_stt_btn = tk.Button(action_frame, text="🗑️ Clear", 
                                 command=lambda: self.stt_output.delete(1.0, tk.END),
                                 bg='#95a5a6', fg='white', font=('Arial', 11, 'bold'), padx=15)
        clear_stt_btn.pack(side=tk.LEFT, padx=5)
    
    def create_settings_tab(self):
        """Create Settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text='⚙️ Settings')
        
        # Voice settings
        voice_frame = tk.LabelFrame(settings_frame, text="Voice Settings", 
                                   font=('Arial', 12, 'bold'), bg='#ecf0f1')
        voice_frame.pack(pady=20, padx=20, fill='x')
        
        # Speech rate
        tk.Label(voice_frame, text="Speech Rate:", font=('Arial', 10), bg='#ecf0f1').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.rate_var = tk.IntVar(value=self.config['voice_rate'])
        rate_scale = tk.Scale(voice_frame, from_=50, to=300, orient=tk.HORIZONTAL, 
                             variable=self.rate_var, command=self.update_voice_rate)
        rate_scale.grid(row=0, column=1, padx=10, pady=5)
        
        # Volume
        tk.Label(voice_frame, text="Volume:", font=('Arial', 10), bg='#ecf0f1').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.volume_var = tk.DoubleVar(value=self.config['voice_volume'])
        volume_scale = tk.Scale(voice_frame, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, 
                               variable=self.volume_var, command=self.update_voice_volume)
        volume_scale.grid(row=1, column=1, padx=10, pady=5)
        
        # Voice selection
        tk.Label(voice_frame, text="Voice:", font=('Arial', 10), bg='#ecf0f1').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.voice_var = tk.StringVar()
        self.voice_combo = ttk.Combobox(voice_frame, textvariable=self.voice_var, state="readonly")
        self.voice_combo.grid(row=2, column=1, padx=10, pady=5)
        self.populate_voices()
        self.voice_combo.bind('<<ComboboxSelected>>', self.update_voice)
        
        # Audio settings
        audio_frame = tk.LabelFrame(settings_frame, text="Audio Settings", 
                                   font=('Arial', 12, 'bold'), bg='#ecf0f1')
        audio_frame.pack(pady=20, padx=20, fill='x')
        
        # Microphone test
        mic_test_btn = tk.Button(audio_frame, text="🎤 Test Microphone", 
                                command=self.test_microphone, bg='#f39c12', fg='white',
                                font=('Arial', 11, 'bold'), padx=20)
        mic_test_btn.pack(pady=10)
        
        # Reset settings
        reset_btn = tk.Button(settings_frame, text="🔄 Reset to Defaults", 
                             command=self.reset_settings, bg='#e67e22', fg='white',
                             font=('Arial', 12, 'bold'), padx=20)
        reset_btn.pack(pady=20)
    
    def create_history_tab(self):
        """Create History tab"""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text='📝 History')
        
        # History listbox
        self.history_listbox = tk.Listbox(history_frame, font=('Arial', 10))
        self.history_listbox.pack(fill='both', expand=True, padx=20, pady=20)
        
        # History buttons
        hist_btn_frame = tk.Frame(history_frame, bg='#ecf0f1')
        hist_btn_frame.pack(pady=10)
        
        refresh_btn = tk.Button(hist_btn_frame, text="🔄 Refresh", 
                               command=self.refresh_history, bg='#3498db', fg='white',
                               font=('Arial', 11, 'bold'), padx=15)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        clear_hist_btn = tk.Button(hist_btn_frame, text="🗑️ Clear History", 
                                  command=self.clear_history, bg='#e74c3c', fg='white',
                                  font=('Arial', 11, 'bold'), padx=15)
        clear_hist_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = tk.Button(hist_btn_frame, text="💾 Export History", 
                              command=self.export_history, bg='#2ecc71', fg='white',
                              font=('Arial', 11, 'bold'), padx=15)
        export_btn.pack(side=tk.LEFT, padx=5)
    
    def setup_tts_settings(self):
        """Configure TTS engine with saved settings"""
        self.tts_engine.setProperty('rate', self.config['voice_rate'])
        self.tts_engine.setProperty('volume', self.config['voice_volume'])
        
        voices = self.tts_engine.getProperty('voices')
        if voices and self.config['voice_id'] < len(voices):
            self.tts_engine.setProperty('voice', voices[self.config['voice_id']].id)
    
    def populate_voices(self):
        """Populate voice selection combobox"""
        voices = self.tts_engine.getProperty('voices')
        voice_names = []
        for i, voice in enumerate(voices):
            name = voice.name if hasattr(voice, 'name') else f"Voice {i+1}"
            voice_names.append(name)
        
        self.voice_combo['values'] = voice_names
        if voice_names:
            self.voice_combo.current(self.config.get('voice_id', 0))
    
    def speak_text(self):
        """Convert text to speech"""
        text = self.tts_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to speak!")
            return
        
        def speak():
            try:
                self.is_speaking = True
                self.speak_btn.config(state='disabled')
                self.status_var.set("Speaking...")
                
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                
                # Add to history
                self.add_to_history("TTS", text)
                
            except Exception as e:
                messagebox.showerror("Error", f"Speech synthesis failed: {str(e)}")
            finally:
                self.is_speaking = False
                self.speak_btn.config(state='normal')
                self.status_var.set("Ready")
        
        threading.Thread(target=speak, daemon=True).start()
    
    def stop_speaking(self):
        """Stop current speech"""
        if self.is_speaking:
            self.tts_engine.stop()
    
    def save_audio(self):
        """Save TTS as audio file"""
        text = self.tts_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to save as audio!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")],
            title="Save Audio File"
        )
        
        if filename:
            try:
                tts = gTTS(text=text, lang='en')
                tts.save(filename)
                messagebox.showinfo("Success", f"Audio saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save audio: {str(e)}")
    
    def toggle_recording(self):
        """Start or stop recording"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start speech recognition"""
        def record():
            try:
                self.is_recording = True
                self.record_btn.config(text="⏹️ Stop Recording", bg='#27ae60')
                self.status_var.set("Listening... Speak now!")
                
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=10)
                
                self.status_var.set("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                
                # Display result
                self.stt_output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {text}\n\n")
                self.stt_output.see(tk.END)
                
                # Add to history
                self.add_to_history("STT", text)
                
                messagebox.showinfo("Success", "Speech recognized successfully!")
                
            except sr.WaitTimeoutError:
                messagebox.showwarning("Timeout", "No speech detected. Please try again.")
            except sr.UnknownValueError:
                messagebox.showwarning("Recognition Error", "Could not understand the speech. Please try again.")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Speech recognition service error: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Recording failed: {str(e)}")
            finally:
                self.is_recording = False
                self.record_btn.config(text="🎙️ Start Recording", bg='#e74c3c')
                self.status_var.set("Ready")
        
        threading.Thread(target=record, daemon=True).start()
    
    def stop_recording(self):
        """Stop recording (handled automatically by the recording thread)"""
        pass
    
    def upload_audio(self):
        """Upload and process audio file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Audio files", "*.wav *.mp3 *.flac *.m4a"), ("All files", "*.*")],
            title="Select Audio File"
        )
        
        if filename:
            def process_audio():
                try:
                    self.status_var.set("Processing audio file...")
                    
                    with sr.AudioFile(filename) as source:
                        audio = self.recognizer.record(source)
                    
                    text = self.recognizer.recognize_google(audio)
                    
                    # Display result
                    self.stt_output.insert(tk.END, f"[File: {os.path.basename(filename)}] {text}\n\n")
                    self.stt_output.see(tk.END)
                    
                    # Add to history
                    self.add_to_history("STT (File)", text)
                    
                    messagebox.showinfo("Success", "Audio file processed successfully!")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to process audio file: {str(e)}")
                finally:
                    self.status_var.set("Ready")
            
            threading.Thread(target=process_audio, daemon=True).start()
    
    def insert_phrase(self, phrase):
        """Insert quick phrase into TTS text box"""
        current_text = self.tts_text.get(1.0, tk.END).strip()
        if current_text:
            self.tts_text.insert(tk.END, f" {phrase}")
        else:
            self.tts_text.insert(1.0, phrase)
    
    def copy_to_tts(self):
        """Copy STT output to TTS input"""
        stt_text = self.stt_output.get(1.0, tk.END).strip()
        if stt_text:
            # Extract just the recognized text (remove timestamps and labels)
            lines = stt_text.split('\n')
            clean_text = []
            for line in lines:
                if '] ' in line:
                    clean_text.append(line.split('] ', 1)[1])
            
            self.tts_text.delete(1.0, tk.END)
            self.tts_text.insert(1.0, ' '.join(clean_text))
            
            # Switch to TTS tab
            self.notebook.select(0)
    
    def save_text(self):
        """Save STT output as text file"""
        text = self.stt_output.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No text to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Text File"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Success", f"Text saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save text: {str(e)}")
    
    def update_voice_rate(self, value):
        """Update TTS speech rate"""
        self.config['voice_rate'] = int(value)
        self.tts_engine.setProperty('rate', int(value))
        self.save_config()
    
    def update_voice_volume(self, value):
        """Update TTS volume"""
        self.config['voice_volume'] = float(value)
        self.tts_engine.setProperty('volume', float(value))
        self.save_config()
    
    def update_voice(self, event=None):
        """Update selected voice"""
        selection = self.voice_combo.current()
        self.config['voice_id'] = selection
        
        voices = self.tts_engine.getProperty('voices')
        if voices and selection < len(voices):
            self.tts_engine.setProperty('voice', voices[selection].id)
        
        self.save_config()
    
    def test_microphone(self):
        """Test microphone functionality"""
        def test():
            try:
                self.status_var.set("Testing microphone...")
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                messagebox.showinfo("Microphone Test", "Microphone is working properly!")
            except Exception as e:
                messagebox.showerror("Microphone Error", f"Microphone test failed: {str(e)}")
            finally:
                self.status_var.set("Ready")
        
        threading.Thread(target=test, daemon=True).start()
    
    def reset_settings(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            self.config = {
                'voice_rate': 200,
                'voice_volume': 0.9,
                'voice_id': 0,
                'theme': 'dark'
            }
            
            # Update UI
            self.rate_var.set(200)
            self.volume_var.set(0.9)
            self.voice_combo.current(0)
            
            # Update TTS engine
            self.setup_tts_settings()
            self.save_config()
            
            messagebox.showinfo("Reset Complete", "Settings have been reset to defaults!")
    
    def add_to_history(self, type_str, text):
        """Add entry to history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': type_str,
            'text': text[:100] + "..." if len(text) > 100 else text
        }
        self.history.append(entry)
        
        # Keep only last 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        self.save_history()
        self.refresh_history()
    
    def refresh_history(self):
        """Refresh history display"""
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.history):
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
            display_text = f"[{timestamp}] {entry['type']}: {entry['text']}"
            self.history_listbox.insert(0, display_text)
    
    def clear_history(self):
        """Clear all history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all history?"):
            self.history = []
            self.save_history()
            self.refresh_history()
    
    def export_history(self):
        """Export history to file"""
        if not self.history:
            messagebox.showwarning("Warning", "No history to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")],
            title="Export History"
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.history, f, indent=2)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        for entry in self.history:
                            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                            f.write(f"[{timestamp}] {entry['type']}: {entry['text']}\n\n")
                
                messagebox.showinfo("Success", f"History exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export history: {str(e)}")

def main():
    root = tk.Tk()
    app = VoiceConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
