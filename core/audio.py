import edge_tts
import asyncio
import os
import re
from pydub import AudioSegment

# DO NOT hardcode ffmpeg.exe here for deployment.
# Streamlit Cloud uses the version installed via packages.txt automatically.

async def synthesize_podcast(script: str, output_path: str = "data/briefing.mp3"):
    # 1. Clean the text
    clean_script = re.sub(r'[#*]', '', script)
    
    # 2. Split logic - using a more flexible regex for 'Host A' or 'Host B'
    raw_segments = re.split(r'(Host [A|B]):', clean_script)
    
    # DEBUG: See if the split actually worked
    print(f"DEBUG: Found {len(raw_segments)//2} dialogue segments.")
    
    combined_audio = AudioSegment.empty()
    temp_files = []

    if not os.path.exists("data"): os.makedirs("data")

    # 3. Process segments
    for i in range(1, len(raw_segments), 2):
        label = raw_segments[i].strip()
        text = raw_segments[i+1].strip().replace("Alex:", "").replace("Sam:", "")
        
        if len(text) < 2: continue # Skip empty lines

        voice = "en-US-AndrewNeural" if "A" in label else "en-US-AvaNeural"
        temp_file = f"data/temp_{i}.mp3"
        
        # Save clip
        communicate = edge_tts.Communicate(text, voice, rate="+10%")
        await communicate.save(temp_file)
        
        # Stitch
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
            segment_audio = AudioSegment.from_mp3(temp_file)
            combined_audio += segment_audio + AudioSegment.silent(duration=500)
            temp_files.append(temp_file)

    # 4. Fallback: If for some reason it's still 0s, add a tiny bit of silence 
    # so the export doesn't create a 'broken' 0-byte file.
    if len(combined_audio) == 0:
        print("WARNING: No audio was generated. Check if 'Host A:' exists in script.")
        combined_audio = AudioSegment.silent(duration=1000)

    combined_audio.export(output_path, format="mp3")
    
    for f in temp_files: 
        try: os.remove(f)
        except: pass
            
    return output_path