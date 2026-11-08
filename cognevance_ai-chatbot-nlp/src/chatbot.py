"""The chatbot: intent recognition + response generation."""
import json
import random
import re
from datetime import datetime

import joblib

from src import config as cfg


class Chatbot:
    def __init__(self, model_path=cfg.MODEL_PATH, intents_path=cfg.INTENTS_PATH,
                 threshold=cfg.CONFIDENCE_THRESHOLD, seed=None):
        self.model = joblib.load(model_path)
        data = json.loads(intents_path.read_text(encoding="utf-8"))
        self.responses = {i["tag"]: i["responses"] for i in data["intents"]}
        self.fallback = self.responses[cfg.FALLBACK_INTENT]
        self.threshold = threshold
        self.rng = random.Random(seed)

    # ---- intent recognition -------------------------------------------------
    def predict_intent(self, text: str):
        """Return (intent, confidence). Low confidence -> 'fallback'."""
        probs = self.model.predict_proba([text])[0]
        best = probs.argmax()
        intent, conf = self.model.classes_[best], float(probs[best])
        if conf < self.threshold:
            return cfg.FALLBACK_INTENT, conf
        return intent, conf

    # ---- small piece of memory: the user's name -----------------------------
    @staticmethod
    def extract_name(text: str):
        m = re.search(r"\b(?:my name is|i am called|call me|this is)\s+([A-Za-z]+)", text, re.I)
        return m.group(1).capitalize() if m else None

    # ---- response generation ------------------------------------------------
    def respond(self, text: str, state: dict = None) -> dict:
        state = state if state is not None else {}
        text = (text or "").strip()
        if not text:
            return {"intent": "empty", "confidence": 1.0, "reply": "Please type something."}

        name = self.extract_name(text)
        if name:
            state["name"] = name
            return {"intent": "introduce_user", "confidence": 1.0,
                    "reply": f"Nice to meet you, {name}! How can I help you?"}

        intent, conf = self.predict_intent(text)
        if intent == cfg.FALLBACK_INTENT:
            reply = self.rng.choice(self.fallback)
        else:
            now = datetime.now()
            user = state.get("name")
            reply = self.rng.choice(self.responses[intent]).format(
                time=now.strftime("%I:%M %p").lstrip("0"),
                date=now.strftime("%A, %d %B %Y"),
                name_part=f", {user}" if user else "")
        return {"intent": intent, "confidence": round(conf, 3), "reply": reply}
