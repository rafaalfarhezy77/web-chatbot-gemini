import os
from flask import Flask , render_template , request , jsonify , session
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "SeCrEtKeYsEsSiOn"

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))
model_name = "gemini-2.5-flash-lite"

nama_bot = "ILY"
karakter_bot = f"""Kamu adalah {nama_bot}, chatbot AI yang berperan sebagai teman curhat dan partner refleksi mental.
Tugasmu adalah mendengarkan, memvalidasi perasaan pengguna tanpa membenarkan tindakan yang salah atau berbahaya.
Kamu bukan terapis, bukan penasihat hidup, dan tidak boleh dijadikan pembenaran atas keputusan keliru.
Kamu harus selalu:
Bersikap empatik dan netral
Mendorong refleksi, bukan ketergantungan
Menolak dengan sopan jika diminta membenarkan hal yang salah
Mengingatkan bahwa keputusan tetap ada di pengguna
Menganjurkan bantuan manusia nyata jika situasi berisiko"""

@app.route('/')
def index():
    session['history'] = []
    return render_template('index.html')

@app.route('/chat' , methods=['POST'])
def chat():
    user_message = request.json.get('message') 
    chat_history = session.get('history', [])

    try:
        chat_history.append({"role" : "user" , "parts" : [{"text" : user_message}]})
        
        response = client.models.generate_content(
            model=model_name, 
            contents=chat_history,
            config=types.GenerateContentConfig(
                system_instruction = karakter_bot,
                temperature=0.7
            )
        )
        
        bot_reply = response.text
        
        chat_history.append({"role" : "user" , "parts" : [{"text" : bot_reply}]})
        
        session['history'] = chat_history
        
        return jsonify({"reply" : response.text})
    except Exception as e :
        if "429" in str(e) :
            return jsonify({"reply" : "Maaf ya aku tinggal dulu, jatah harianku habis. Tetep semangat ya kita ngobrol lagi besok :)"})
        return jsonify({"reply" : f"Error nih masbro {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
        