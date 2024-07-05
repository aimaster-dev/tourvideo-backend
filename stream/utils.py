import subprocess
import os
import re
import uuid
import hashlib

processes = {}

def hash_string(rtsp_url):
    return hashlib.sha256(rtsp_url.encode()).hexdigest()

def get_output_dir(rtsp_url):
    hashed_name = hash_string(rtsp_url)
    return f'media/hls/{hashed_name}'

def convert_rtsp_to_hls(rtsp_url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    command = [
        'ffmpeg', '-rtsp_transport', 'tcp', '-analyzeduration', '50000000', '-probesize', '50000000',
        '-i', rtsp_url,
        '-map', '0:v:0', '-map', '0:a:0',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28',
        '-c:a', 'aac', '-ar', '44100', '-b:a', '128k',
        '-f', 'hls', '-hls_time', '4', '-hls_list_size', '3',  # Keep only the last 3 segments
        '-hls_flags', 'delete_segments', '-hls_delete_threshold', '1', # Delete segments once 4 exist
        f'{output_dir}/index.m3u8'
    ]
    
    process = subprocess.Popen(command)
    processes[output_dir] = process
    print(output_dir)

def stop_stream(output_dir):
    print(output_dir)
    process = processes.get(output_dir)
    if process:
        process.terminate()
        process.wait()
        del processes[output_dir]
    if os.path.exists(output_dir):
        for root, dirs, files in os.walk(output_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(output_dir)
