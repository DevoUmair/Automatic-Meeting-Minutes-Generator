import whisper
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp
import aiofiles
import os
import subprocess
import uuid

load_dotenv()
client = OpenAI()
model = whisper.load_model("base")

app = FastAPI()
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows requests only from these origins
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)

class VideoURLRequest(BaseModel):
    video_url: str

async def download_video(url: str, filename: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=400, detail="Failed to download video")
            f = await aiofiles.open(filename, mode='wb')
            await f.write(await resp.read())
            await f.close()

def video_to_audio(video_file):
    audio_file = f"{video_file}.mp3"
    subprocess.call(["ffmpeg", "-y", "-i", video_file, audio_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return audio_file

def audio_to_transcript(audio_file):
    result = model.transcribe(audio_file)
    return result['text']

def Mom_generation(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes meeting transcripts into brief discussion points in bullet format."
            },
            {
                "role": "user",
                "content": f"""From the following transcript, extract only brief and concise discussion points in bullet points.

                            Do not include Agenda, Conclusion, Date, Time, Location, Participants, or Action Items.

                            Transcript:
                            {prompt}"""
            }
        ],
        temperature=0.7,
        max_tokens=700,
    )
    return response.choices[0].message.content

@app.post("/process_summary")
async def process_video_url(request: VideoURLRequest):
    video_file = f"video_{uuid.uuid4()}.mp4"
    try:
        # Download video from URL
        await download_video(request.video_url, video_file)

        # Extract audio from video
        audio_file = video_to_audio(video_file)

        # Transcribe audio
        transcript = audio_to_transcript(audio_file)

        # Generate summary
        summary = Mom_generation(transcript)

        # Clean up temp files
        os.remove(video_file)
        os.remove(audio_file)

        # Format response for HTML
        html_result = summary.replace("\n", "<br>")
        return {"response": html_result}
    except Exception as e:
        # Remove files if exist on failure
        if os.path.exists(video_file):
            os.remove(video_file)
        return {"error": str(e)}

