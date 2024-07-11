#!/usr/bin/env python3
from openai import OpenAI
from dotenv import load_dotenv
import os

# SETUP
# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
user_prompt = "always return as list in JSON format"
detailed_prompt = "Break down each JSON object, look up and give me detailed history on each object"

# Check if the API key is loaded
if not api_key:
    raise ValueError("API key not found. Make sure you have an OPENAI_API_KEY in your .env file.")

# BEGIN
print(f"Welcome to the show, a few functional and purpose notes:" '\n' 
"1: This program will call OpenAI LLM to generate a list of definitions for you" '\n'
"2: These answers will output to a text file." '\n'
"3: Further detailed itemization of each lookup is avalible with the detailed option." '\n')

file_out = input(f"Specify file output name:" '\n')

key_list = []

def openAIcall(prompt, user_input):
    # OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
        )

        # Extract the message content
        message = response.choices[0].message.content

        # Format the message
        formatted_message = message.strip()
        reformat = '}{[],"'
        for char in reformat:
            formatted_message = formatted_message.replace(char, "")
        print(formatted_message)

        global key_list
        key_list = message.split('"')  # Split into words (need to figure out how to split it into )
        key_list = [item for item in key_list if item]  # Remove empty strings

        # Append outputs to a file
        with open(f'./{file_out}', 'a') as f:
            for item in key_list:
                f.write(f"{item}")
        print(f"Written {user_input} to {file_out}")
        return message
    except Exception as e:
        print(f"An error occurred: {e}")

def detailedOpenAIcall(prompt, file_content):
    # OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": file_content}
            ]
        )

        # Extract the message content
        message = response.choices[0].message.content
        return message
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        user_input = input("Options at this prompt:" '\n' "'reset' to" '\n' "'exit' to quit" '\n' "'yes' to continue" '\n'
          "'detailed' to get detailed itemization on each object in a file" '\n').strip().lower()

        if user_input == "yes":
            user_input2 = input("What are you looking for?\n")
            openAIcall(user_prompt, user_input2)
            continue

        if user_input == "reset":
            print("Resetting the program...")
            with open(f'./{file_out}', 'w') as f:
                f.write(f"")
            continue  # Restart the loop, effectively resetting the program

        if user_input == "exit":
            print("Exiting.")
            reset_input = input("Do you want to exit the program? (yes/no): ").strip().lower()
            if reset_input != "no":
                print("Exiting the program...")
                break
            #exits program
            continue

        if user_input == "detailed":
            file_in = input(f"Specify file input name:" '\n')
            try:
                # Open both read and write files and define their objects
                with open(file_in, 'r') as fileread, open(file_out, 'a') as filewrite:
                    file_content = fileread.read()
                    response = detailedOpenAIcall(detailed_prompt, file_content.strip())
                    if response:
                        print(f"{response}" '\n')
                        filewrite.write(response + '\n')
            except FileNotFoundError:
                print(f"File not found: {file_in}")
            except Exception as e:
                print(f"An error occurred while processing: {e}")
            continue

        print("Not an option" '\n' '\n')

if __name__ == "__main__":
    main()  # Run the main function