# ============================
# Converts Video Files to WEBP
# Version 1 - 9.29.2025
# by Kjell Boersma
# ============================

# ============================
# This script converts video files to animated WebP format using ffmpeg.
# It provides a GUI file selector to choose the input video file.
# The script maintains aspect ratio and allows customization of frame rate.
# The output WebP will be created in the same directory as the input video.
# Requirements: ffmpeg must be installed and accessible from command line.
# ============================


import os
import subprocess
import tkinter as tk
from tkinter import filedialog

# Function to select video file
def select_video_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv;*.flv;*.wmv")]
    )
    return file_path

# Function to convert video to animated WebP
def convert_video_to_webp(input_video_path, output_webp_path, fps=20, width=800, height=600):
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_video_path,
        '-vcodec', 'libwebp',
        '-filter:v', f'fps=fps={fps}',
        '-lossless', '1',
        '-loop', '0',
        '-preset', 'default',
        '-an',
        '-vsync', '0',
        '-s', f'{width}:{height}',
        output_webp_path
    ]
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Conversion successful: {output_webp_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

# Function to get video dimensions using ffprobe
def get_video_dimensions(video_path):
    command = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0:s=x',
        video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    dimensions = result.stdout.strip()
    width, height = map(int, dimensions.split('x'))
    return width, height

# Main function
if __name__ == "__main__":
    video_file = select_video_file()
    if video_file:
        # Get video dimensions
        width, height = get_video_dimensions(video_file)

        # Define output file path
        output_file = os.path.splitext(video_file)[0] + '.webp'

        # Convert video to animated WebP
        convert_video_to_webp(video_file, output_file, width=width, height=height)
    else:
        print("No video file selected.")