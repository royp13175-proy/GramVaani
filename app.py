import os
import re
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS
from config import Config  # Config file load ki
from modules.scheme_finder import finder
from modules.voice_processor import text_to_speech
from modules.translator import generate_voice_response

app = Flask(__name__)
app.config.from_object(Config)  # Config settings apply ki
CORS(app)

def sanitize_text_for_speech(text):
    if not text:
        return ""
    
    clean_text = text

    # 1. URLs / Links ko audio se hatao (taaki gTTS http/www spell na kare)
    clean_text = re.sub(r'https?://\S+|www\.\S+', '', clean_text)

    # 2. Common Hinglish & Brand Terms Mapping to Devanagari
    replacements = {
        r'\bGramVaani\b': 'ग्रामवाणी',
        r'\bGramvaani\b': 'ग्रामवाणी',
        r'\bgramvaani\b': 'ग्रामवाणी',
        r'\bGramVani\b': 'ग्रामवाणी',
        r'\byojana\b': 'योजना',
        r'\byojanaen\b': 'योजनाएं',
        r'\bkisan\b': 'किसान',
        r'\bsamman\b': 'सम्मान',
        r'\bnidhi\b': 'निधि',
        r'\bpradhanmantri\b': 'प्रधानमंत्री',
        r'\blabh\b': 'लाभ',
        r'\byogyata\b': 'योग्यता',
        r'\bdastawez\b': 'दस्तावेज़',
        r'\brupees\b': 'रुपये',
        r'\bbank\b': 'बैंक',
        r'\baccount\b': 'अकाउंट',
        r'\bpm\b': 'पीएम',
        r'\blink\b': 'लिंक',
        r'\bwebsite\b': 'वेबसाइट'
    }

    for pattern, replacement in replacements.items():
        clean_text = re.sub(pattern, replacement, clean_text, flags=re.IGNORECASE)

    # 3. Bache hue English letters (A-Z) aur special characters ko audio text se remove karein
    clean_text = re.sub(r'[a-zA-Z]', '', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/schemes')
def all_schemes():
    return jsonify(finder.schemes)

@app.route('/api/ask', methods=['POST'])
def ask_bot():
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        lang = data.get('lang', 'hi-IN')
        
        print(f"\n[INFO] User Query: {query} | Lang: {lang}")
        
        # 1. Scheme Matching
        matched_schemes = finder.find(query)
        
        # 2. Response Generation
        raw_response_text = generate_voice_response(matched_schemes, query, lang)
        
        # 3. Audio Text Cleaning (Remove links, Hinglish & English spellout)
        speech_text = sanitize_text_for_speech(raw_response_text)
        
        # Fallback if speech_text gets completely empty
        if not speech_text.strip():
            speech_text = raw_response_text

        # 4. Text to Speech Conversion using gTTS
        audio_url = None
        try:
            # Force gTTS Hindi mode for natural voice
            gtts_lang = 'hi' if ('hi' in lang or any('\u0900' <= c <= '\u097F' for c in speech_text)) else 'en'
            
            # Unique filename to avoid browser caching issues
            audio_filename = f"response_{uuid.uuid4().hex[:8]}.mp3"
            audio_dir = os.path.join('static', 'audio')
            os.makedirs(audio_dir, exist_ok=True)
            
            file_path = os.path.join(audio_dir, audio_filename)
            
            # gTTS Audio Generation
            tts = gTTS(text=speech_text, lang=gtts_lang, slow=False)
            tts.save(file_path)
            
            audio_url = f"/static/audio/{audio_filename}"
            print(f"[INFO] gTTS Audio generated successfully: {audio_url}")
            
        except Exception as tts_error:
            print(f"⚠️ [WARNING] gTTS generation failed, trying module fallback: {tts_error}")
            audio_path = text_to_speech(speech_text, lang)
            if audio_path:
                audio_url = f"/{audio_path}" if not audio_path.startswith('/') else audio_path

        return jsonify({
            'success': True,
            'query': query,
            'response_text': raw_response_text,
            'schemes': matched_schemes,
            'audio_url': audio_url
        })

    except Exception as e:
        print(f"\n❌ [ERROR in /api/ask]: {str(e)}\n")
        return jsonify({
            'success': False,
            'error': str(e),
            'response_text': "क्षमा करें, अभी उत्तर देने में समस्या आ रही है।"
        }), 500

@app.route('/api/voice-to-text', methods=['POST'])
def voice_upload():
    return jsonify({'text': ''})

if __name__ == '__main__':
    os.makedirs('static/audio', exist_ok=True)  # Audio directory ensure ki
    app.run(host='0.0.0.0', port=5000, debug=True)