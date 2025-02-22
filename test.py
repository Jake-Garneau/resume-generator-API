import requests

BASE_URL = "http://127.0.0.1:8000"

state = {
    "resume_data": {
        "personal_info": {
            "name": None,
            "email": None,
            "phone": None,
            "location": None
        },
        "education": [],
        "professional_experience": [],
        "skills": [],
        "interests": []
    },
    "current_section": "personal_info",
    "current_experience_index": -1
}

user_inputs = [
    "First Last",
    "xxx@email.com",
    "123-456-7890",
    "New York, NY",
    "UW Madison",
    "Bachelor's in Computer Science",
    "3.7",
    "May 2025",
    "yes",
    "Google",
    "SWE",
    "August 2021",
    "Present",
    "Developed xxx.",
    "Bullet point 2.",
    "done",
    "Python, Java",
    "AI, interest 2!"
]

def converse(state, user_input):
    url = f"{BASE_URL}/conversation"
    payload = {"state": state, "user_input": user_input}
    response = requests.post(url, json=payload)
    return response.json() if response.ok else None

for user_input in user_inputs:
    print(f"User Input: {user_input}")
    result = converse(state, user_input)
    if not result:
        break
    print(f"Question: {result['question']}")
    state = result["state"]

print("\nFinal State:")
print(state)