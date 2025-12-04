import tkinter as tk
from src.ui import SpeechToTextUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextUI(root)
    app.run()