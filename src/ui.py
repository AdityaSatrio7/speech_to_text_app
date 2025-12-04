# Disini script untuk buat user interface aplikasi

import tkinter as tk
from tkinter import font
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os

class SpeechToTextUI:
    def __init__(self,root):
        self.root = root
        self.root.title("Speech to Text APP")
        
        #Set ukuran minimum dan konfigurasi root
        self.root.minsize(900, 550)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        #Track tombol aktif/tidak aktif
        self.is_recording = False
        
        #Tab bar lime green
        top_bar = tk.Frame(self.root, bg="#8BE41f", height=40)
        top_bar.grid(row=0, column=0, sticky="ew")
        
        #Background utama
        main = tk.Frame(self.root, bg="#0B6EDF")
        main.grid(row=1, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=1)  
        
        #frame di dalam main
        content = tk.Frame(main, bg="#0B6EDF")
        content.grid(row=0, column=0, pady=20, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(2, weight=1)
        
        #Teks Judul
        font_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "Italianno-Regular.ttf"
        )
        
        try:
            title_font = font.Font(
                file =font_path,
                size =40
            )
        except:
            title_font = ("Segoe Script", 40, "italic")
            
        title_label = tk.Label(
            content,
            text="Text-to-Speech Aditya I. S.",
            font=title_font,
            fg="#F2FA11",
            bg="#0B6EDF"
        )
        title_label.grid(row=0, column=0, pady=(10, 5))
        
        #Teks untuk pesan error
        self.error_label = tk.Label(
            content,
            text="",
            fg="#F81717",
            bg="#0B6EDF",
            font=("Segoe UI", 20, "bold")
        )
        self.error_label.grid(row=1, column=0, pady=(0, 10))
        
        #Container untuk tombol dan teks area
        box = tk.Frame(
            content,
            bg="#E3DEBC",
            bd=0,
            highlightthickness=0
        )
        box.grid(row=2, column=0, padx=80, pady=10, sticky="nsew")
        box.columnconfigure(0, weight=1)
        box.rowconfigure(0, weight=1)
        box.rowconfigure(1, weight=0)
        
        #widget teks area pakai scroll
        self.text_box = ScrolledText(
            box,
            wrap="word",
            font=("Segoe UI", 12),
            bg="#E3DEBC",
            borderwidth=0,
            height=1  
        )
        self.text_box.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        #Placeholder text
        self.PLACEHOLDER_IDLE = "Tekan tombol mic untuk mulai merekam"
        self.PLACEHOLDER_RECORDING = "Merekam..."
        
        #Set initial placeholder text
        self._show_placeholder_idle()
        
        #Load icon tombol
        self._load_icons()
        
        #Tombol mulai/berhenti rekam
        self.record_button = tk.Button(
            box,
            image=self.mic_icon,
            bd=0,
            bg="#E3DEBC",
            activebackground="#E3DEBC",
            command=self.toggle_record_state
        )
        self.record_button.grid(row=1, column=0, sticky="e",padx=20, pady=(0, 20))
        
        #Untuk penggunaan di controller
        self._record_start_callback = None
        self._record_stop_callback = None
    
    #Method untuk load icon
    def _load_icons(self):
        asset_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets"
        )
        
        mic_path = os.path.join(asset_dir, "mic_icon.png")
        stop_path = os.path.join(asset_dir, "stop_icon.png")
        
        self.mic_icon = ImageTk.PhotoImage(Image.open(mic_path).resize((40, 40)))
        self.stop_icon = ImageTk.PhotoImage(Image.open(stop_path).resize((40, 40)))
    
    #Method yang dipanggil saat tombol ditekan
    def toggle_record_state(self):
        if not self.is_recording:
            #Mulai merekam
            self.record_button.config(image=self.stop_icon)
            self.is_recording = True
            self._show_placeholder_recording()
            
            if self._record_start_callback:
                self._record_start_callback()
        else:
            #Berhenti merekam
            self.record_button.config(image=self.mic_icon)
            self.is_recording = False
            self._show_placeholder_idle()
            
            if self._record_stop_callback:
                self._record_stop_callback()
    
    #Method untuk menampilkan placeholder saat idle (belum recording)
    def _show_placeholder_idle(self):
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert("1.0", self.PLACEHOLDER_IDLE)
        self.text_box.config(state="disabled")
    
    #Method untuk menampilkan placeholder saat recording
    def _show_placeholder_recording(self):
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert("1.0", self.PLACEHOLDER_RECORDING)
        self.text_box.config(state="disabled")
    
    #Method-method yang bakal dipanggil controller
    def set_record_start_callback(self, cb):
        self._record_start_callback = cb
    
    def set_record_stop_callback(self, cb):
        self._record_stop_callback = cb
        
    #Function untuk display text
    def display_text(self, text):
        self.text_box.config(state="normal")
        # Bersihin placeholder ganti sama text dari audio
        if self.text_box.get("1.0", tk.END).strip() in [self.PLACEHOLDER_IDLE, self.PLACEHOLDER_RECORDING]:
            self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, text + "\n")
        self.text_box.see(tk.END)
    
    def display_error(self, msg):
        self.error_label.config(text=msg)
        
    def clear_error(self):
        self.error_label.config(text="")
        
    def run(self):
        self.root.mainloop()       