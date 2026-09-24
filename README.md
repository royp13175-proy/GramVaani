# GramVaani - AI Voice-Bot for Government Schemes

ग्रामीण भारत के लिए बनाया गया एक AI Voice Assistant जो सरकारी योजनाओं की जानकारी हिंदी आवाज़ में देता है।

## Features

- 🎙️ Voice Input (Hindi + English) - Web Speech API
- 🔊 Voice Output (TTS) - gTTS
- 🔍 Intelligent Scheme Search - RapidFuzz matching
- 🌐 Hindi + English Support
- 📱 Mobile Friendly UI
- 🗃️ JSON based schemes database (easily extensible)

## Project Structure

```
GramVaani/
├── app.py                 # Main Flask App
├── config.py
├── schemes_data.json      # 5 sample schemes (extendable to 100+)
├── requirements.txt
├── modules/
│   ├── voice_processor.py # TTS logic
│   ├── scheme_finder.py   # Fuzzy search
│   └── translator.py      # Response generator
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/script.js
```

## Setup Instructions (VS Code / Local)

1. Python 3.9+ install karein
2. Project folder me terminal open karein:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
3. Browser me open karein: http://127.0.0.1:5000

## How It Works

1. User mic dabakar bolta hai: "Mujhe ghar ki yojana chahiye"
2. Frontend Web Speech API se text banata hai
3. Backend RapidFuzz se schemes_data.json me search karta hai
4. Response Hindi me generate hota hai + gTTS se MP3 banta hai
5. Frontend me text + audio + scheme cards dikhte hain

## Extend Kaise Karein?

- `schemes_data.json` me aur yojanayein add karein
- `app.py` me OpenAI / Sarvam AI API add karke LLM response la sakte hain
- WhatsApp Bot banana ho to Twilio integration add karein

## Deployment

- Render / Railway / PythonAnywhere par Flask app deploy kar sakte hain
- For offline village kiosk, isse Raspberry Pi par bhi chala sakte hain
