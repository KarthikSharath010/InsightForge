import edge_tts
import asyncio
import os
import re
from pydub import AudioSegment

# DO NOT hardcode ffmpeg.exe here for deployment.
# Streamlit Cloud uses the version installed via packages.txt automatically.

async def synthesize_podcast(script: str, output_path: str = "data/briefing.mp3"):
    """
    Parses dialogue, assigns neural voices (Alex & Sam), 
    and stitches a professional master track.
    """
    
    # 1. Clean markdown and structural headers
    clean_script = re.sub(r'[#*]', '', script)
    clean_script = clean_script.replace("PART 2: PODCAST SCRIPT", "").strip()
    
    # 2. Parse dialogue segments
    # Splitting by "Host A:" or "Host B:"
    raw_segments = re.split(r'(Host [A|B]):', clean_script)
    
    combined_audio = AudioSegment.empty()
    temp_files = []

    # Ensure data directory exists for temp files
    if not os.path.exists("data"):
        os.makedirs("data")

    # 3. Voice Orchestration
    for i in range(1, len(raw_segments), 2):
        label = raw_segments[i].strip()
        text_to_speak = raw_segments[i+1].strip()
        
        if not text_to_speak: continue

        # Identity Assignment: Host A = Alex (Male), Host B = Sam (Female)
        voice = "en-US-AndrewNeural" if "A" in label else "en-US-AvaNeural"
        
        temp_file = f"data/temp_{i}.mp3"
        
        # Synthesize ONLY the dialogue
        communicate = edge_tts.Communicate(text_to_speak, voice, rate="+10%")
        await communicate.save(temp_file)
        
        # Stitch with natural conversational pacing
        segment_audio = AudioSegment.from_mp3(temp_file)
        combined_audio += segment_audio + AudioSegment.silent(duration=450)
        temp_files.append(temp_file)

    # 4. Final Master Export
    combined_audio.export(output_path, format="mp3")
    
    # Clean up temp assets
    for f in temp_files: 
        if os.path.exists(f): os.remove(f)
            
    return output_path