import requests
import json

with open('questions.json', 'r') as f:
    questions = json.load(f)

# Only the questions which have the word "Response timed out."
#questions = [x for x in questions if 'Response timed out.' in questions[x]]

for question in questions:
    print(question)

# Skip the first # questions (Replace # with the number of questions to skip)
#questions = questions[#:]

print("Starting LLAMA 2 querying with", len(questions), "questions")

# Read in saved LLAMA 2 dictionary from answers.json
with open('answers.json', 'r') as f:
    llama = json.load(f)

# Asking questions and writing answers to answers.json
for question in questions:

    html_str = requests.get("http://localhost:5041/chat?q=" + question).text    
    llama[question] = html_str

    with open('answers.json', 'w', encoding='utf-8') as f:
        json.dump(llama, f, ensure_ascii=False, indent=4)
