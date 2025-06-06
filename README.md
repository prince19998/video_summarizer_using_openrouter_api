# Video Summarizer

A Flask-based web application that automatically transcribes and summarizes video/audio recordings of meetings. The application uses AI to extract key points and action items from meeting recordings.

## Features

- Upload video/audio files (supports MP3, MP4, WAV, M4A formats)
- Automatic transcription using Whisper API via OpenRouter
- AI-powered meeting summary generation
- Extraction of key points and action items
- Clean and intuitive web interface
- Database storage for meeting records and summaries

## Prerequisites

- Python 3.7 or higher
- OpenRouter API key
- SQLite (default) or any other SQL database

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd video_summarizer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your-secret-key
OPENROUTER_API_KEY=your-openrouter-api-key
LLM_MODEL=openai/gpt-3.5-turbo  # or your preferred model
DATABASE_URL=sqlite:///meetings.db  # or your database URL
```

5. Initialize the database:
```bash
flask init-db
```

## Usage

1. Start the Flask application:
```bash
flask run
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a video/audio file of your meeting

4. Wait for the processing to complete (transcription and summary generation)

5. View the extracted key points and action items

## Project Structure

```
video_summarizer/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── .flaskenv          # Flask environment variables
├── static/            # Static files (CSS, JS)
│   └── styles.css
└── templates/         # HTML templates
    └── index.html
```

## API Integration

The application uses OpenRouter API for:
- Audio transcription (Whisper API)
- Text summarization (GPT models)

## Database Schema

### Meeting Table
- id (Primary Key)
- filename
- upload_time
- status

### Summary Table
- id (Primary Key)
- meeting_id (Foreign Key)
- key_points
- action_items
- generated_at

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 