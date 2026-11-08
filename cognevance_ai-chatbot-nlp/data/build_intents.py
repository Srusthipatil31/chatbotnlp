"""Builds data/intents.json from the readable dictionary below.

Edit INTENTS to add or change what the chatbot knows, then re-run:
    python data/build_intents.py && python main.py
Placeholders usable in responses: {time}, {date}, {name_part} (", Name" or empty)
"""
import json
from pathlib import Path

INTENTS = {
 "greeting": {
  "patterns": ["hi", "hello", "hey", "good morning", "good evening", "hey there", "hi bot", "hello there",
               "greetings", "howdy", "good afternoon", "hiya", "hello bot"],
  "responses": ["Hello{name_part}! I'm Cogni. How can I help you today?",
                "Hi{name_part}! Nice to see you. What can I do for you?",
                "Hey{name_part}! Ask me about courses, internships, fees or anything else."]},
 "goodbye": {
  "patterns": ["bye", "goodbye", "see you later", "see you", "talk to you later", "i have to go",
               "catch you later", "good night", "bye bye", "i am leaving", "farewell", "that is all see you"],
  "responses": ["Goodbye{name_part}! Come back any time.", "See you later{name_part}! Have a great day.",
                "Bye{name_part}! Happy learning."]},
 "thanks": {
  "patterns": ["thanks", "thank you", "thanks a lot", "thank you so much", "appreciate it", "that helped thanks",
               "great thanks", "many thanks", "thx", "cheers", "thanks for the help", "awesome thank you"],
  "responses": ["You're welcome!", "Happy to help!", "Anytime! Let me know if you need anything else."]},
 "bot_name": {
  "patterns": ["what is your name", "who are you", "what should i call you", "tell me your name",
               "may i know your name", "are you a bot", "are you human", "introduce yourself",
               "what are you called", "your name please", "who am i talking to"],
  "responses": ["I'm Cogni, a chatbot built with Python and NLP.",
                "My name is Cogni. I'm a virtual assistant, not a human."]},
 "capabilities": {
  "patterns": ["what can you do", "how can you help me", "what are your features", "what do you do",
               "what can i ask you", "list your abilities", "what are you capable of", "what topics do you know",
               "show me what you can do", "what services do you provide", "what kind of questions can you answer"],
  "responses": ["I can answer questions about courses, fees, enrollment, refunds, certificates and internships, "
                "tell the time and date, share a joke, and explain basic AI/ML ideas."]},
 "creator": {
  "patterns": ["who made you", "who created you", "who built you", "who is your developer", "who programmed you",
               "who is your creator", "who developed this chatbot", "how were you made",
               "what technology are you built with", "how do you work internally", "who is behind you"],
  "responses": ["I was built as a Python NLP project: text is cleaned, converted to TF-IDF features and "
                "classified into intents by a machine-learning model.",
                "A student developer built me using Python, scikit-learn and Flask."]},
 "courses": {
  "patterns": ["what courses do you offer", "tell me about your courses", "which courses are available",
               "list of programs", "what can i learn here", "do you have python courses",
               "available training programs", "show me the course catalog", "what subjects do you teach",
               "are there machine learning courses", "course list please", "i want to know about courses"],
  "responses": ["We offer Python programming, Data Science, Machine Learning, AI & NLP and Web Development. "
                "Each course has beginner, intermediate and advanced levels."]},
 "pricing": {
  "patterns": ["how much does it cost", "what are the fees", "course fees", "what is the price", "is it free",
               "do you have discounts", "how much do i have to pay", "pricing details", "cost of the program",
               "tell me the fee structure", "are there any scholarships", "what are the charges"],
  "responses": ["Fees depend on the course and level. Some beginner modules are free, and scholarships are "
                "available for students. Please check the pricing page for exact amounts."]},
 "enrollment": {
  "patterns": ["how do i enroll", "how can i register", "i want to join a course", "sign up process",
               "how to apply", "how do i sign up", "enrollment steps", "where do i register",
               "i want to enroll", "registration process", "admission procedure", "how can i join"],
  "responses": ["To enroll: 1) create an account, 2) pick a course, 3) pay the fee or apply for a scholarship, "
                "4) start learning right away."]},
 "refund": {
  "patterns": ["i want a refund", "how do i get my money back", "refund policy", "can i cancel my enrollment",
               "cancel my subscription", "money back guarantee", "how to cancel the course",
               "i want to cancel and get a refund", "do you give refunds", "cancellation policy",
               "return my payment", "i paid by mistake"],
  "responses": ["You can request a full refund within 7 days of enrollment if you have completed less than "
                "20% of the course. Contact support with your order ID."]},
 "certificate": {
  "patterns": ["do i get a certificate", "will i receive a certificate", "certificate after completion",
               "is the certificate valid", "how do i download my certificate", "certification details",
               "do you provide certificates", "course completion certificate", "where is my certificate",
               "can i get a certificate for the internship", "is there a certification"],
  "responses": ["Yes! You receive a digital certificate after completing all modules and passing the final "
                "assessment. You can download it from your profile page."]},
 "internship": {
  "patterns": ["do you offer internships", "tell me about internships", "how to apply for an internship",
               "internship opportunities", "are internships paid", "i am looking for an internship",
               "internship duration", "remote internship available", "how long is the internship",
               "internship projects", "can students do internships", "internship application"],
  "responses": ["We run remote internships for students in AI/ML, data science and web development. "
                "Interns complete real projects, submit them on GitHub and receive a completion certificate."]},
 "contact_support": {
  "patterns": ["i need to talk to support", "how can i contact you", "customer support number", "support email",
               "i want to speak to a human", "contact details", "how do i reach support",
               "i have a problem with my account", "i need help from an agent", "give me your email address",
               "talk to a person", "customer care contact"],
  "responses": ["You can reach our support team at support@example.com. Replace this with your real contact "
                "details in data/intents.json."]},
 "working_hours": {
  "patterns": ["what are your working hours", "when are you open", "support timings", "what time do you open",
               "are you available on weekends", "opening hours", "when can i call", "business hours",
               "is support available 24 hours", "what time do you close", "office timings",
               "when is support available"],
  "responses": ["Our support team is available Monday to Saturday, 9 AM to 6 PM. I'm available 24/7."]},
 "time": {
  "patterns": ["what time is it", "tell me the time", "current time", "what is the time now",
               "do you know the time", "can you tell me the time", "time please", "what is the time right now"],
  "responses": ["It's {time} right now."]},
 "date": {
  "patterns": ["what is the date today", "today's date", "what day is it", "tell me the date",
               "which day is today", "what is today's date", "current date", "can you tell me the date",
               "what day is today"],
  "responses": ["Today is {date}."]},
 "joke": {
  "patterns": ["tell me a joke", "make me laugh", "say something funny", "i want to hear a joke",
               "got any jokes", "joke please", "tell me something funny", "crack a joke",
               "can you tell a joke", "i need a laugh", "entertain me", "funny joke"],
  "responses": ["Why do programmers prefer dark mode? Because light attracts bugs!",
                "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
                "Why did the data scientist bring a ladder? To reach the high-level features!"]},
 "weather": {
  "patterns": ["what is the weather", "how is the weather today", "will it rain today", "weather forecast",
               "is it sunny outside", "temperature today", "tell me the weather", "is it going to rain",
               "how hot is it", "weather in my city", "what is the temperature", "do i need an umbrella"],
  "responses": ["I can't check live weather because I'm not connected to a weather service. "
                "A weather app will give you an accurate forecast."]},
 "programming_help": {
  "patterns": ["how do i learn python", "best way to learn programming", "which language should i start with",
               "tips for learning to code", "how do i become a programmer", "where to start coding",
               "how to learn coding", "i am a beginner in programming", "advice for new programmers",
               "how to get better at coding", "recommend a programming language", "is python good for beginners"],
  "responses": ["Start with Python: learn variables, loops, functions and data structures, then build small "
                "projects every week. Practising daily matters more than long, rare sessions."]},
 "ai_info": {
  "patterns": ["what is machine learning", "explain artificial intelligence", "what is ai",
               "define machine learning", "what is deep learning", "difference between ai and ml",
               "tell me about nlp", "what is natural language processing", "how does machine learning work",
               "explain neural networks", "what is a chatbot", "what is data science"],
  "responses": ["AI is the broad goal of making machines act intelligently. Machine learning is a part of AI "
                "where models learn patterns from data. NLP applies ML to human language, which is how I "
                "understand your messages."]},
 "mood_good": {
  "patterns": ["i am fine", "i am doing great", "feeling good", "i am good", "doing well", "all good",
               "i feel happy", "i am great how about you", "pretty good today", "i am doing good",
               "feeling awesome", "i am happy"],
  "responses": ["Glad to hear that! What would you like to know?", "That's great! How can I help?"]},
 "mood_bad": {
  "patterns": ["i am sad", "i feel bad", "not feeling good", "i am stressed", "i am tired",
               "having a bad day", "i feel lonely", "i am upset", "i am feeling down", "i am not okay",
               "i am worried", "feeling low"],
  "responses": ["I'm sorry you're feeling that way. Taking a short break or talking to someone you trust can "
                "help. I'm here if you'd like to chat or need help with anything."]},
 "how_are_you": {
  "patterns": ["how are you", "how are you doing", "how is it going", "how do you do", "are you okay",
               "how are you today", "hope you are doing well", "how have you been", "how is your day",
               "and you", "how do you feel"],
  "responses": ["I'm doing great, thanks for asking! How about you?", "All good here! How can I help you?"]},
 "affirm": {
  "patterns": ["yes", "yeah", "sure", "okay", "ok", "yes please", "of course", "definitely", "sounds good",
               "correct", "that is right", "absolutely"],
  "responses": ["Great! What would you like to know?", "Okay! Go ahead."]},
 "deny": {
  "patterns": ["no", "nope", "no thanks", "not really", "i don't think so", "never mind", "no thank you",
               "not now", "nah", "i do not want that", "maybe later", "skip it"],
  "responses": ["No problem. Let me know if you change your mind.", "Alright, I'm here if you need me."]},
 "help": {
  "patterns": ["help", "i need help", "can you help me", "help me please", "i need some assistance",
               "assist me", "i am confused", "i need guidance", "could you help", "please help",
               "i have a question", "can i ask you something"],
  "responses": ["Of course! Tell me what you need. I can talk about courses, fees, enrollment, refunds, "
                "certificates and internships."]},
}

FALLBACK = ["Sorry, I didn't understand that. Could you rephrase? You can ask about courses, fees, "
            "enrollment, refunds, certificates or internships.",
            "Hmm, I'm not sure about that one. Try asking about our courses, internships or support."]


# ---- extra training examples (more data = better recognition) -------------------
EXTRA = {
 "creator": ["which tools were used to build you", "what language are you written in", "what framework powers you"],
 "courses": ["do you teach machine learning", "do you provide web development classes", "what classes are offered",
             "which topics can i study here"],
 "pricing": ["any student discount", "do you give discounts to students", "is there a payment plan",
             "what do i need to pay", "is there any scholarship for students"],
 "enrollment": ["i would like to join", "i wish to register", "how do i become a student", "sign me up",
                "how can i take admission"],
 "certificate": ["are the certificates accredited", "is the certificate recognized by companies",
                 "will i get a completion letter", "can i share my certificate on linkedin"],
 "internship": ["is the internship unpaid", "internship eligibility", "who can apply for the internship",
                "is there any stipend for interns", "what do interns work on"],
 "help": ["i require some help", "need assistance", "can someone help me", "i am stuck and need support"],
 "goodbye": ["okay talk later", "see you soon", "take care bye", "i am logging off now"],
 "thanks": ["i really appreciate it", "much obliged", "that is very kind of you", "thanks buddy"],
 "bot_name": ["am i chatting with a machine", "are you a real person", "are you an ai", "do you have a name"],
 "capabilities": ["what are you able to answer", "what questions do you handle"],
 "contact_support": ["how do i get in touch with your team", "i would like to speak with customer care"],
 "working_hours": ["are you open on public holidays", "what are your support hours on saturday"],
 "mood_bad": ["i am having a rough time", "i feel anxious", "today was horrible"],
 "mood_good": ["everything is going well", "i feel fantastic", "life is good"],
 "how_are_you": ["how is life treating you", "how are things with you"],
}
for tag, pats in EXTRA.items():
    INTENTS[tag]["patterns"] += pats

# Out-of-scope class: teaches the model what it should NOT try to answer.
INTENTS["fallback"] = {
 "patterns": ["what is the capital of japan", "who is the prime minister", "who won the cricket world cup",
              "book a hotel room for me", "order a pizza", "what is the price of gold", "how do i bake a cake",
              "play my favourite song", "translate hello into french", "latest news headlines",
              "should i invest in shares", "what is 25 times 4", "recommend a good movie",
              "who is the richest person", "how tall is mount everest", "what is the speed of light",
              "i want to buy a phone", "directions to the nearest hospital", "write an essay about dogs",
              "random words blah blah", "lorem ipsum dolor", "zxcvb nmlkj", "how many people live in india",
              "who is your favourite actor", "what is the best car", "solve this equation for me",
              "how do i lose weight", "tell me a story about a dragon", "what are the lottery numbers",
              "who is the best football player", "how to fix my car engine", "what is the population of china",
              "give me a recipe for biryani", "tell me about the election", "how far is the moon"],
 "responses": FALLBACK}

out = {"intents": [{"tag": t, "patterns": d["patterns"], "responses": d["responses"]} for t, d in INTENTS.items()],
       "fallback_responses": FALLBACK}
path = Path(__file__).with_name("intents.json")
path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {path} | {len(INTENTS)} intents, {sum(len(d['patterns']) for d in INTENTS.values())} patterns")
