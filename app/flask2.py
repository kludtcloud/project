#!/usr/bin/env python3

import openai
from dotenv import load_dotenv
import os
from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__)

# SETUP
# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key not found. Make sure you have an OPENAI_API_KEY in your .env file.")

# Set OpenAI API key
openai.api_key = api_key

@app.route('/')
def my_form():
    return render_template('my-form2.html')

@app.route('/submit', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()

    prompt = "Return results in JSON"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": processed_text}
            ]
        )

        # Extract the message content
        message = response.choices[0].message['content']

        # Save the message in a session or pass it via URL parameters
        return redirect(url_for('/results', result=message))
        
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/results')
def results():
    result = request.args.get('result')
    return render_template('results.html', result=result)

#def detailedOpenAIcall(prompt, file_content):
#    try:
#        response = openai.ChatCompletion.create(
#            model="gpt-3.5-turbo",
#            messages=[
#                {"role": "system", "content": prompt},
#                {"role": "user", "content": file_content}
#            ]
#        )
#
#       # Extract the message content
#        message = response.choices[0].message['content']
#        return message
#    except Exception as e:
#       print(f"An error occurred: {e}")
#        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2224, debug=True)