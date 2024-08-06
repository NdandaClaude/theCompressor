import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
    if file_path:
        file_label.config(text=file_path)
        compress_button.config(state='normal')

def compress_video():
    input_path = file_label.cget("text")
    if not input_path:
        messagebox.showerror("Error", "Please select a file first.")
        return
    
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if output_path:
        if getattr(sys, 'frozen', False):
            ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
        else:
            ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
        
        if not os.path.isfile(ffmpeg_path):
            messagebox.showerror("Error", "FFmpeg executable not found at the specified path.")
            return
        command = [
            ffmpeg_path, '-i', input_path,
            '-vcodec', 'libx264', '-crf', '32', '-preset', 'veryslow',
            '-b:a', '96k', '-s', '640x360',
            output_path
        ]
        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", "Compression completed successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Compression failed: {e}")

root = tk.Tk()
root.title("Video Compressor")
root.geometry("400x250")
root.configure(bg="#2c3e50")

root.eval('tk::PlaceWindow . center')

style_label = {"bg": "#2c3e50", "fg": "white", "font": ("Helvetica", 12)}
style_button = {"bg": "#2980b9", "fg": "white", "font": ("Helvetica", 10), "relief": "raised", "bd": 3}

file_label = tk.Label(root, text="Select a video file...", **style_label)
file_label.pack(pady=20)

select_button = tk.Button(root, text="Select File", command=select_file, **style_button)
select_button.pack(pady=10)

compress_button = tk.Button(root, text="Compress Video", state='disabled', command=compress_video, **style_button)
compress_button.pack(pady=10)

root.mainloop()
