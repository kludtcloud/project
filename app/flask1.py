#!/usr/bin/env python3

from openai import OpenAI


from dotenv import load_dotenv
import os
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# SETUP
# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
if not api_key:
    raise ValueError("API key not found. Make sure you have an OPENAI_API_KEY in your .env file.")

# Set OpenAI API key

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text

    prompt = "Return detailed results"
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": processed_text}
        ])

        # Extract the message content
        message = response.choices[0].message.content

        # Properly format JSON
        json_message = message.strip()
        key_list = json_message.split('"')  # Split into words (need to figure out how to split it into )
        key_list = [item for item in key_list if item]  # Remove empty strings

        file_out = "output.txt"
        # Append outputs to a file
        with open(file_out, 'a') as f:
            for item in key_list:
                f.write(f"{item}\n")

        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)})

def detailedOpenAIcall(prompt, file_content):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": file_content}
        ])

        # Extract the message content
        message = response.choices[0].message.content
        return message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2224)