from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import requests
from models import db, Meeting, Summary
from config import Config
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'mp3', 'mp4', 'wav', 'm4a'}

def transcribe_audio(filepath):
    """Transcribe audio using Whisper API via OpenRouter"""
    headers = {
        "Authorization": f"Bearer {app.config['OPENROUTER_API_KEY']}",
        "Content-Type": "audio/wav"  # Convert to WAV first in production
    }
    
    with open(filepath, 'rb') as f:
        response = requests.post(
            "https://openrouter.ai/api/v1/audio/transcriptions",
            headers=headers,
            files={"file": f}
        )
    
    if response.status_code == 200:
        return response.json().get("text", "")
    raise Exception(f"Transcription failed: {response.text}")

def generate_summary(text):
    """Generate summary using LLM via OpenRouter"""
    headers = {
        "Authorization": f"Bearer {app.config['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": app.config['LLM_MODEL'],
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful meeting assistant. Extract key points and action items from the transcript."
            },
            {
                "role": "user",
                "content": f"""Analyze this meeting transcript and return JSON with:
                - "key_points": array of 3-5 main discussion points
                - "action_items": array of tasks with owners if mentioned
                
                Transcript: {text}"""
            }
        ],
        "temperature": 0.3
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return json.loads(content)
    raise Exception(f"Summary failed: {response.text}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file uploaded")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No file selected")
        
        if not allowed_file(file.filename):
            return render_template('index.html', error="Unsupported file type")
        
        try:
            # Save file temporarily
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Create meeting record
            meeting = Meeting(
                filename=filename,
                upload_time=datetime.utcnow(),
                status="processing"
            )
            db.session.add(meeting)
            db.session.commit()
            
            # Transcribe and summarize
            transcript = transcribe_audio(filepath)
            summary = generate_summary(transcript)
            
            # Save results
            summary_record = Summary(
                meeting_id=meeting.id,
                key_points="\n".join(summary.get("key_points", [])),
                action_items="\n".join(summary.get("action_items", [])),
                generated_at=datetime.utcnow()
            )
            db.session.add(summary_record)
            meeting.status = "completed"
            db.session.commit()
            
            # Clean up
            os.remove(filepath)
            
            return render_template('index.html', 
                               key_points=summary.get("key_points", []),
                               action_items=summary.get("action_items", []))
            
        except Exception as e:
            if 'meeting' in locals():
                meeting.status = "failed"
                db.session.commit()
            return render_template('index.html', error=str(e))
    
    return render_template('index.html')

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
    print("Database initialized.")

if __name__ == '__main__':
    app.run()