"""CodSoft AI Internship - Task 1: Rule-Based Chatbot
Uses regex pattern matching (if/else style rules) to reply to user input."""
import re
import random
from datetime import datetime

# Each rule: (regex pattern, list of possible replies). First match wins.
RULES = [
    (r"\b(hi|hello|hey|hola|namaste)\b",
     ["Hello! How can I help you today?", "Hi there! What's on your mind?"]),
    (r"\bhow are you\b",
     ["I'm just code, but I'm running great! How about you?"]),
    (r"\bmy name is (\w+)",
     ["Nice to meet you, {0}!", "Great to meet you, {0}. How can I help?"]),
    (r"\b(what('s| is) your name|who are you)\b",
     ["I'm CodBot, a rule-based chatbot built for the CodSoft AI internship."]),
    (r"\b(time)\b", ["__TIME__"]),
    (r"\b(date|today|day)\b", ["__DATE__"]),
    (r"\b(help|can you do|features)\b",
     ["I can chat, tell the time/date, tell jokes, do simple math "
      "(try: calc 12 * 7), and answer a few questions about AI."]),
    (r"\bjoke\b",
     ["Why do programmers prefer dark mode? Because light attracts bugs!",
      "Why did the AI go to school? To improve its learning rate!"]),
    (r"\b(what is|define) (ai|artificial intelligence)\b",
     ["AI is the field of making machines perform tasks that normally need "
      "human intelligence - learning, reasoning, perception and language."]),
    (r"\b(machine learning|ml)\b",
     ["Machine learning is a branch of AI where models learn patterns from data "
      "instead of being explicitly programmed."]),
    (r"\b(python)\b",
     ["Python is the most popular language for AI thanks to libraries like "
      "NumPy, scikit-learn, TensorFlow and PyTorch."]),
    (r"\b(thanks|thank you)\b", ["You're welcome!", "Happy to help!"]),
    (r"\b(bye|goodbye|exit|quit)\b", ["Goodbye! Have a great day!"]),
]

FALLBACKS = ["Sorry, I didn't understand that. Try asking for 'help'.",
             "Hmm, I don't have a rule for that yet. Could you rephrase?"]


def safe_calc(expr: str) -> str:
    if not re.fullmatch(r"[\d\s+\-*/().%]+", expr):
        return "I can only calculate with numbers and + - * / ( ) %."
    try:
        return f"Result: {eval(expr, {'__builtins__': {}}, {})}"
    except Exception:
        return "That doesn't look like a valid calculation."


def respond(text: str) -> str:
    text = text.strip().lower()
    if not text:
        return "Say something and I'll reply!"
    m = re.match(r"calc(?:ulate)?\s+(.+)", text)
    if m:
        return safe_calc(m.group(1))
    for pattern, replies in RULES:
        match = re.search(pattern, text)
        if match:
            reply = random.choice(replies)
            if reply == "__TIME__":
                return "It's " + datetime.now().strftime("%I:%M %p") + "."
            if reply == "__DATE__":
                return "Today is " + datetime.now().strftime("%A, %d %B %Y") + "."
            groups = [g.capitalize() for g in match.groups() if g]
            return reply.format(*groups) if "{0}" in reply else reply
    return random.choice(FALLBACKS)


def main():
    print("CodBot: Hi! I'm CodBot. Type 'help' for options, 'bye' to exit.")
    while True:
        user = input("You: ")
        reply = respond(user)
        print("CodBot:", reply)
        if re.search(r"\b(bye|goodbye|exit|quit)\b", user.lower()):
            break


if __name__ == "__main__":
    main()
