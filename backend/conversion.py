# conversion.py
import subprocess
import os
import shutil
from logger import log_info, log_error

def convert_webm_to_wav(input_path: str) -> str:
    # Ensure input file exists
    if not os.path.exists(input_path):
        log_info(f"Input file {input_path} not found")  # added logging
        raise FileNotFoundError(f"Input file {input_path} not found")
    
    log_info(f"Starting conversion for {input_path}")  # added logging
    
    # Create a new filename for the WAV file
    wav_path = os.path.splitext(input_path)[0] + ".wav"
    
    # Check if ffmpeg is installed
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not found in PATH. Please install it or add it to your PATH.")
    
    # Use subprocess.run with list arguments to handle file paths reliably
    command = ["ffmpeg", "-y", "-i", input_path, wav_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        log_info(f"ffmpeg error: {result.stderr.strip()}")  # added logging
        raise Exception(result.stderr.strip())
    
    log_info(f"Conversion completed: {wav_path}")  # added logging
    
    return wav_path
