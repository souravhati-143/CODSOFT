# ============================================================
#  CodSoft AI Internship — Task 1: Rule-Based Chatbot
#  Author : (Your Name)
#  Description: A simple rule-based chatbot using pattern
#               matching and if-else logic.
# ============================================================

import re
import random
import datetime

# ── greeting responses ────────────────────────────────────────
GREETINGS = ["Hello! How can I help you today?",
             "Hey there! What can I do for you?",
             "Hi! Nice to meet you. Ask me anything!"]

# ── farewell responses ────────────────────────────────────────
FAREWELLS = ["Goodbye! Have a great day!",
             "See you later! Take care!",
             "Bye! It was nice chatting with you!"]

# ── unknown input responses ───────────────────────────────────
UNKNOWN = ["I'm not sure I understand. Could you rephrase that?",
           "Hmm, I don't know about that yet. Try asking something else!",
           "I didn't quite get that. Can you try again?"]

# ─────────────────────────────────────────────────────────────
#  Pattern → Response rules
#  Each entry: (compiled regex, list of possible responses)
# ─────────────────────────────────────────────────────────────
RULES = [
    # Greetings
    (re.compile(r'\b(hello|hi|hey|howdy|greetings)\b', re.I),
     GREETINGS),

    # Farewells
    (re.compile(r'\b(bye|goodbye|see you|farewell|exit|quit)\b', re.I),
     FAREWELLS),

    # How are you
    (re.compile(r'\bhow are you\b', re.I),
     ["I'm doing great, thanks for asking! How about you?",
      "I'm just a bot, but I'm feeling fantastic! How can I help?"]),

    # Name
    (re.compile(r'\bwhat.*(your name|are you called)\b', re.I),
     ["I'm ChatBot, your friendly AI assistant!",
      "You can call me ChatBot. Nice to meet you!"]),

    # Age
    (re.compile(r'\bhow old are you\b', re.I),
     ["I was born the day I was coded — age is just a number for bots!",
      "I don't age. Lucky me!"]),

    # Time
    (re.compile(r'\bwhat.*time\b', re.I),
     [lambda: f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."]),

    # Date
    (re.compile(r'\bwhat.*date|today.*date\b', re.I),
     [lambda: f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."]),

    # Weather (static — no API)
    (re.compile(r'\bweather\b', re.I),
     ["I don't have live weather data, but I suggest checking Google Weather or weather.com!"]),

    # Jokes
    (re.compile(r'\btell.*joke|joke\b', re.I),
     ["Why do programmers prefer dark mode? Because light attracts bugs! 😄",
      "Why was the computer cold? It left its Windows open! 😂",
      "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads!"]),

    # Thanks
    (re.compile(r'\b(thanks|thank you|thx|ty)\b', re.I),
     ["You're welcome! 😊", "Happy to help!", "Anytime! Let me know if you need anything else."]),

    # Help
    (re.compile(r'\bhelp\b', re.I),
     ["Sure! You can ask me about:\n"
      "  • Greetings / Farewells\n"
      "  • Current time and date\n"
      "  • Jokes\n"
      "  • General questions\n"
      "Just type anything and I'll do my best!"]),

    # AI / what can you do
    (re.compile(r'\bwhat can you do|your abilities|capabilities\b', re.I),
     ["I can chat with you, tell jokes, share the time and date, and answer simple questions. I'm learning every day!"]),

    # Python
    (re.compile(r'\bpython\b', re.I),
     ["Python is a fantastic programming language! Great choice for AI projects.",
      "Python is the language of AI and data science. You're on the right track!"]),

    # AI / Artificial Intelligence
    (re.compile(r'\bartificial intelligence|machine learning|deep learning\b', re.I),
     ["AI is the future! It involves teaching machines to learn from data and make decisions.",
      "Machine learning is a subset of AI where systems learn patterns from data. Exciting stuff!"]),

    # CodSoft
    (re.compile(r'\bcodsoft\b', re.I),
     ["CodSoft is an amazing platform for internships and skill development!",
      "CodSoft provides great opportunities for budding developers. Keep up the good work!"]),
]


# ─────────────────────────────────────────────────────────────
#  Core chatbot function
# ─────────────────────────────────────────────────────────────
def get_response(user_input: str) -> str:
    """Match user input against rules and return a response."""
    user_input = user_input.strip()

    if not user_input:
        return "Please type something so I can help you!"

    for pattern, responses in RULES:
        if pattern.search(user_input):
            reply = random.choice(responses)
            # Support lambda (dynamic) responses
            return reply() if callable(reply) else reply

    return random.choice(UNKNOWN)


# ─────────────────────────────────────────────────────────────
#  Main chat loop
# ─────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  Welcome to ChatBot — CodSoft AI Internship")
    print("  Type 'quit' or 'bye' to exit.")
    print("=" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nChatBot: Goodbye! Have a great day!")
            break

        if not user_input:
            continue

        response = get_response(user_input)
        print(f"ChatBot: {response}")

        # Exit keywords
        if re.search(r'\b(bye|goodbye|exit|quit)\b', user_input, re.I):
            break


if __name__ == "__main__":
    main()