import os
import yt_dlp
import tkinter as tk
from tkinter import messagebox, filedialog

def list_available_resolutions(url):
    ydl_opts = {}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        
        video_formats = [f for f in info_dict['formats'] if f['vcodec'] != 'none' and f['acodec'] == 'none']
        
        available_resolutions = {
            '1': {'label': '4K', 'resolution': '2160p', 'height': 2160},
            '2': {'label': '2K', 'resolution': '1440p', 'height': 1440},
            '3': {'label': 'FullHD', 'resolution': '1080p', 'height': 1080},
            '4': {'label': 'SD', 'resolution': '480p', 'height': 480}
        }
        
        resolutions = {}
        for key, res in available_resolutions.items():
            for format in video_formats:
                if format['height'] == res['height']:
                    resolutions[key] = res
                    resolutions[key]['format_id'] = format['format_id']  # Voeg format_id toe
                    print(f"Found resolution: {res['label']} with format_id: {format['format_id']}")  # Debug info
                    break
        
        return resolutions

def download_video(url, format_id, download_path):
    if format_id:
        ydl_opts = {
            'format': f'{format_id}+bestaudio',
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'overwrites': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Fout", "Voer een geldige YouTube-link in")
        return

    resolutions = list_available_resolutions(url)
    
    if not resolutions:
        messagebox.showwarning("Fout", "Geen beschikbare resoluties gevonden")
        return
    
    resolution_choice = resolution_var.get()
    
    if resolution_choice not in resolutions:
        messagebox.showwarning("Fout", "Kies een geldige resolutie")
        return

    download_path = filedialog.askdirectory()
    if not download_path:
        messagebox.showwarning("Fout", "Selecteer een downloadlocatie")
        return
    
    format_id = resolutions[resolution_choice].get('format_id')
    
    if not format_id:
        messagebox.showwarning("Fout", "Geen format_id gevonden voor de geselecteerde resolutie")
        return
    
    download_video(url, format_id, download_path)
    
    messagebox.showinfo("Succes", "Video gedownload!")

# GUI Setup
root = tk.Tk()
root.title("YouTube Downloader")

# URL invoer
tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Resolutiekeuze
tk.Label(root, text="Kies resolutie:").grid(row=1, column=0, padx=10, pady=10)
resolution_var = tk.StringVar(value="1")

tk.Radiobutton(root, text="4K", variable=resolution_var, value="1").grid(row=1, column=1, sticky='w')
tk.Radiobutton(root, text="2K", variable=resolution_var, value="2").grid(row=2, column=1, sticky='w')
tk.Radiobutton(root, text="FullHD", variable=resolution_var, value="3").grid(row=3, column=1, sticky='w')
tk.Radiobutton(root, text="SD", variable=resolution_var, value="4").grid(row=4, column=1, sticky='w')

# Download knop
download_button = tk.Button(root, text="Download", command=start_download)
download_button.grid(row=5, column=1, padx=10, pady=10)

# Start de GUI-loop
root.mainloop()
