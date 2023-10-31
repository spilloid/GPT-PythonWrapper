# app.py
from chat_components import ChatComponent, Message, ChatComposite, ChatVisitor
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Initialize
app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")
root = ChatComposite()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    root.add(Message('User', user_message))

    # GPT-3.5 Interaction
    messages = [{"role": "system", "content": "You are an intelligent assistant."}]
    messages.append({"role": "user", "content": user_message})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    assistant_reply = chat.choices[0].message['content']

    root.add(Message('Assistant', assistant_reply))

    # Visitor
    visitor = ChatVisitor()
    root.accept(visitor)

    return jsonify({'status': 'success','message': assistant_reply})
if __name__ == '__main__':
    app.run(debug=True)

