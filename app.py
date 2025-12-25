import os
from flask import Flask , render_template , request , jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat' , methods=['POST'])
def chat():
    user_message = request.json.get('message')
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=user_message
        )
        return jsonify({"reply" : response.text})
    except Exception as e :
        return jsonify({"reply" : f"Error nih masbro {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
        