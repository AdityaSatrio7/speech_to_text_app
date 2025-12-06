#Script ini untuk menghandle logic dari speech to text

import json
import threading
import pyaudio
from vosk import Model, KaldiRecognizer

class SpeechEngine:
    def __init__(self, model_path="model"):
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.audio_interface = None
        self.stream = None
        
        self._listening = False
        self._thread = None
        
    def initialize(self):
        # Load model vosk
        try:
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, 16000)
        except Exception as e:
            raise RuntimeError(f"Gagal memuat model Vosk: {e}")
        
        # Inisialisasi pyaudio
        self.audio_interface = pyaudio.PyAudio()
        self.stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        self.stream.start_stream()
        
    def start_listening(self, callback):
        if self._listening:
            return # Sudah mendengar
        self._listening = True
        
        def listen_loop():
            while self._listening:
                data = self.stream.read(4000, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        callback(text)
                else:
                    # Handle audio partial
                    partial = json.loads(self.recognizer.PartialResult())
                    text = partial.get("partial", "").strip()
                    if text:
                        callback(text)
        
        self._thread = threading.Thread(target=listen_loop, daemon=True)
        self._thread.start()
        
    def stop_listening(self):
        if not self._listening:
            return
        self._listening = False
        
        # Tunggu thread selesai
        if self._thread is not None:
            self._thread.join()
        # Stop streaming suara
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        # Tutup Pyaudio
        if self.audio_interface is not None:
            self.audio_interface.terminate()            