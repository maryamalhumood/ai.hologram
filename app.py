import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key here (loaded from environment variables)
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Initialize Flask app
app = Flask(__name__)

# Store AI response temporarily
latest_answer = ""

# Route for Website 1 (Question Page)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the question from the form
        user_input = request.form.get('question')

        if user_input:
            try:
                # Get AI response from OpenAI API
                chat_completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Update this to gpt-4 if desired
                    messages=[{"role": "user", "content": user_input}]
                )
                global latest_answer
                latest_answer = chat_completion['choices'][0]['message']['content']
                print(f"AI Response: {latest_answer}")  # Debug print to check AI response

                # Generate speech using OpenAI Text-to-Speech API
                speech_file_path = Path("static/speech.mp3")
                tts_response = openai.Audio.speech.create(
                    model="tts-1",
                    voice="ash",
                    input=latest_answer,
                )
                tts_response.stream_to_file(speech_file_path)

            except Exception as e:
                latest_answer = f"Error: {str(e)}"
        return render_template('index.html')
    return render_template('index.html')

# Route for Website 2 (Hologram Response Page)
@app.route('/ai-response')
def ai_response():
    global latest_answer
    return render_template('index3.html', answer=latest_answer)

# Route to fetch the AI answer as JSON
@app.route('/get-answer')
def get_answer():
    return jsonify({"answer": latest_answer})

if __name__ == '__main__':
    # Run the app on port 5000 (default) or any other port you want
    app.run(host='0.0.0.0', port=5000, debug=True)
