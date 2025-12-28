import edge_tts
import asyncio
import os

async def synthesize_audio(script: str, output_name: str = "briefing.mp3"):
    """Converts script to professional neural audio"""
    output_path = os.path.join("data", output_name)
    # Using 'AndrewNeural' for a professional corporate voice
    communicate = edge_tts.Communicate(script, "en-US-AndrewNeural")
    await communicate.save(output_path)
    return output_path