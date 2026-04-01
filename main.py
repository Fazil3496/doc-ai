import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('login.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        image_data = request.json['image']
        # Updated for Medical Report Analysis
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are a professional medical consultant. Analyze this medical report image. Explain the findings in simple terms as a doctor would. List potential concerns and recommended next steps. Disclaimer: For informational purposes only."
                        },
                        {"type": "image_url", "image_url": {"url": image_data}}
                    ]
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        return jsonify({"description": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"description": f"Connection Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)