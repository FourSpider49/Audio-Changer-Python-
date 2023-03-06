import pyaudio
import numpy as np
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk

chunk_size = 1024
pitch_factor = 0.5 # Change this value to adjust pitch

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    shifted_data = np.roll(audio_data, int(chunk_size / pitch_factor))
    return (shifted_data.tobytes(), pyaudio.paContinue)

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                output=True,
                frames_per_buffer=chunk_size,
                stream_callback=callback)

r = sr.Recognizer()

# GUI setup
window = tk.Tk()
window.title("Voice Changer")
window.configure(bg="#282828")

# Labels
title_label = tk.Label(window, text="Voice Changer", font=("Arial", 20), bg="#282828", fg="white")
title_label.pack(pady=10)

instruction_label = tk.Label(window, text="Speak something to hear your voice changed:", font=("Arial", 12), bg="#282828", fg="white")
instruction_label.pack()

output_label = tk.Label(window, text="", font=("Arial", 12), bg="#282828", fg="white")
output_label.pack(pady=10)

# Button
def recognize():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            output_label.config(text=f"Original: {text}")
            stream.write(audio.get_raw_data())
            output_label.config(text=f"Original: {text}\nChanged: {text} (pitch shifted)")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            
recognize_button = ttk.Button(window, text="Start", command=recognize)
recognize_button.pack(pady=10)

window.mainloop()

stream.stop_stream()
stream.close()

p.terminate()
