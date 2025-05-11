# 🎥📝 Meeting Minutes Generator from Video using FastAPI, Whisper, and GPT-3.5

This project is a FastAPI-based web application that allows you to upload a meeting video, extract its audio, transcribe the speech to text using OpenAI Whisper, and generate structured **Minutes of Meeting (MoM)** using OpenAI's GPT-3.5.

---

## 📌 Features

- Upload a meeting video (`.mp4`)
- Extract audio using FFmpeg
- Transcribe audio to text using Whisper
- Summarize transcript into:
  - **Agenda**
  - **Discussion Points**
  - **Conclusion**
- Clean HTML output suitable for frontend display

---

## 🚀 Tech Stack

- Python 3.11+
- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [OpenAI GPT-3.5](https://platform.openai.com/docs/guides/gpt)
- [FFmpeg](https://ffmpeg.org/)

---

## 📂 Project Structure

```
├── app.py               # Main FastAPI server
├── .env                 # API key for OpenAI
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/DevoUmair/Automatic-Meeting-Minutes-Generator.git
cd meeting-minutes-generator
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

- **Windows**: Download from [FFmpeg official site](https://ffmpeg.org/download.html) and add it to your system PATH.
- **Linux/macOS**: Use a package manager:
```bash
sudo apt install ffmpeg  # Debian/Ubuntu
brew install ffmpeg      # macOS
```

### 5. Add OpenAI API Key

Create a `.env` file in the root folder:

```
OPENAI_API_KEY=your-openai-api-key-here
```

---

## ▶️ Run the App

```bash
uvicorn app:app --reload
```

Access the API at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 How to Use the API

### Endpoint: `POST /upload_video`

Upload a video file using Postman, Curl, or a frontend. Example:

#### ✅ Request:

- Type: `multipart/form-data`
- Field: `file` → your `.mp4` file

#### ✅ Response:

```json
{
  "response": "**Agenda:**<br>- Point 1<br>**Discussion Points:**<br>- Point A<br>**Conclusion:**<br>- Summary here"
}
```

---

## 🧠 Example Output

```html
**Agenda:**<br>
- Setting up Olamma for LLM deployment<br>
- Training steps with Unsloth<br><br>

**Discussion Points:**<br>
- Using LLM3 8-bit models with LoRA adapters<br>
- Preparing datasets using Alpaca format<br>
- Using Google Colab for local training<br><br>

**Conclusion:**<br>
- Ready to convert model for Olamma<br>
- Encouragement to explore further
```

---

## 📝 `requirements.txt`

```txt
openai
whisper
fastapi
python-dotenv
uvicorn
aiofiles
```

---

## 🛠 Notes

- Uses Whisper `base` model for speed. Switch to `medium` or `large` for better accuracy.
- GPT model used: `gpt-3.5-turbo`.
- Max token limit is set to 700 to control output length and API usage.

---

## 📃 License

This project is licensed under the MIT License.

---

## 🙌 Credits

- [OpenAI](https://openai.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Whisper ASR](https://github.com/openai/whisper)
- [FFmpeg](https://ffmpeg.org/)
