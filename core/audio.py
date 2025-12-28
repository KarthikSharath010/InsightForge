import edge_tts
import asyncio
import os
import re
from pydub import AudioSegment

# Link local executables
AudioSegment.converter = os.path.abspath("ffmpeg.exe")
AudioSegment.ffprobe = os.path.abspath("ffprobe.exe")

async def synthesize_podcast(script: str, output_path: str = "data/briefing.mp3"):
    # 1. Strip all structural headers and markdown
    clean_script = re.sub(r'[#*]', '', script)
    clean_script = clean_script.replace("PART 2: PODCAST SCRIPT", "").strip()
    
    # 2. Split into Host segments
    raw_segments = re.split(r'(Host [A|B]):', clean_script)
    combined_audio = AudioSegment.empty()
    temp_files = []

    for i in range(1, len(raw_segments), 2):
        label = raw_segments[i].strip()
        text_to_speak = raw_segments[i+1].strip()
        
        if not text_to_speak: continue

        # FINAL POLISH: Strip the names from the spoken text so they don't say "Alex: Hello"
        text_to_speak = text_to_speak.replace("Alex:", "").replace("Emma:", "").strip()

        # Assign Voices: Andrew for Host A (Alex), Ava for Host B (Emma)
        voice = "en-US-AndrewNeural" if "A" in label else "en-US-AvaNeural"
        
        temp_file = f"data/temp_{i}.mp3"
        communicate = edge_tts.Communicate(text_to_speak, voice, rate="+10%")
        await communicate.save(temp_file)
        
        segment_audio = AudioSegment.from_mp3(temp_file)
        combined_audio += segment_audio + AudioSegment.silent(duration=450)
        temp_files.append(temp_file)

    combined_audio.export(output_path, format="mp3")
    for f in temp_files: os.remove(f)
    return output_path