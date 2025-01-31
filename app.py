import os
from flask import Flask, render_template, request, send_file, jsonify
import openai
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Initialize Flask app
app = Flask(__name__)

# Store AI response temporarily
latest_answer = ""

# Generate audio using OpenAI's TTS with Ash voice
def generate_tts(text, filename="speech.mp3"):
    try:
        # Use the correct TTS model, e.g., "text-to-speech"
        response = openai.Audio.create(
            model="text-to-speech-1",  # Correct TTS model
            voice="ash",  # Ash voice
            input=text,
        )
        
        # Save the audio file
        speech_file_path = Path(__file__).parent / filename
        with open(speech_file_path, 'wb') as audio_file:
            audio_file.write(response['data'])
        
        return speech_file_path
    except Exception as e:
        return f"Error: {str(e)}"

# Route for Website 1 (Question Page)
@app.route('/', methods=['GET', 'POST'])
def index():
    global latest_answer
    if request.method == 'POST':
        user_input = request.form.get('question')

        if user_input:
            try:
                # Get AI response from OpenAI API
                chat_completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_input}]
                )
                latest_answer = chat_completion['choices'][0]['message']['content']
                print(f"AI Response: {latest_answer}")

                # Generate audio for the AI response using the Ash voice
                generate_tts(latest_answer)

            except Exception as e:
                latest_answer = f"Error: {str(e)}"
        return render_template('index.html')
    return render_template('index.html')

# Route for Website 2 (Hologram Response Page)
@app.route('/ai-response')
def ai_response():
    global latest_answer
    return render_template('index3.html', answer=latest_answer)

# Route to serve the audio file
@app.route('/get-audio')
def get_audio():
    return send_file("speech.mp3", as_attachment=False)

# New route to fetch the latest AI response
@app.route('/latest-answer')
def get_latest_answer():  # Function name changed to resolve conflict
    return jsonify({'answer': latest_answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
