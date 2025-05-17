import whisper
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
import subprocess
from fastapi import FastAPI , File , UploadFile
import aiofiles
import json

load_dotenv()
client = OpenAI()
model  = whisper.load_model("base")

app = FastAPI()

def video_to_audio(video_file):
    audio_file = "input_audio.mp3"
    subprocess.call(["ffmpeg", "-y", "-i", video_file, audio_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )
    return audio_file


def audio_to_transcript(audio_file):
    result = model.transcribe(audio_file)
    transcript = result['text']
    return transcript

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


@app.post("/upload_video")
async def upload_video(file: UploadFile = File(...)):
    fileName = file.filename
    async with aiofiles.open(fileName, mode="wb") as f:
        await f.write(await file.read())

    audio_file = video_to_audio(fileName)
    transcript = audio_to_transcript(audio_file)
    final_result = Mom_generation(transcript)

    # Convert newlines to HTML <br> tags
    html_result = final_result.replace("\n", "<br>")
    return {"response": html_result}