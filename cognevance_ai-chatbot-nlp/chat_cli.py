"""Chat in the terminal.   python chat_cli.py   (type 'quit' to exit)"""
from src.chatbot import Chatbot

bot, state = Chatbot(), {}
print("Cogni: Hi! Ask me about courses, fees, internships... (type 'quit' to exit)")
while True:
    try:
        text = input("You : ").strip()
    except (EOFError, KeyboardInterrupt):
        break
    if text.lower() in {"quit", "exit", "q"}:
        break
    r = bot.respond(text, state)
    print(f"Cogni: {r['reply']}   [{r['intent']} {r['confidence']:.2f}]")
