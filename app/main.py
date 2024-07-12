#!/usr/bin/python3.8

#import libraiers 
from openai import OpenAI
from dotenv import load_dotenv
#read .env files
import os
from datetime import date
#os allows read write of files

#flask is local webserver, request, redirect, render_templates are functions to return pages
#session creates a individual session for each connection (aka user)
#jsonify is a pass through for the JSON code output to the HTML page
from flask import Flask, request, render_template, jsonify, redirect, session, url_for
import json

date = date.today()
#intialize the flask called "app"
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key not found. Make sure you have an OPENAI_API_KEY in your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

#landing page used base.html + "my-form.html" to render
@app.route('/')
def my_form():
    return render_template('my-form.html')

#POST aka "user submit button" takes 'text' submission from html form and pasees it to the openAI function
@app.route('/', methods=['POST'])
def my_form_post():
    #sets 'text' to input from html in my-form submission
    text = request.form['text']
    #confgiures the directive sent to the API, we can adjust output based on this
    prompt = "Return only detailed results in JSON and break down each item in a subsection and define, no pre context of message input"
    try:
        #call the API
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ])

        # Extract the message content
        message = response.choices[0].message.content

        # Format JSON response
        json_message = json.loads(message)

        file_out = f"output{date}.txt"
        # Append outputs to a file
        with open(file_out, 'a') as f:
            json.dump(json_message, f, indent=4)

        session['message'] = json_message
        return redirect(url_for('results'))
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/results", methods=['GET'])
def results():
    message = session.get('message', None)
    return render_template('results.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
