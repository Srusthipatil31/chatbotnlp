"""Run:  python -m unittest discover -s tests -v"""
import unittest

from src.chatbot import Chatbot
from src.preprocess import preprocess


class PreprocessTests(unittest.TestCase):
    def test_lowercase_and_punctuation(self):
        self.assertEqual(preprocess("HELLO!!!"), preprocess("hello"))

    def test_contractions_and_slang(self):
        self.assertIn("thank", preprocess("thx"))
        self.assertIn("do not", preprocess("I don't know"))


class ChatbotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = Chatbot(seed=0)

    def intent(self, text):
        return self.bot.respond(text, {})["intent"]

    def test_core_intents(self):
        cases = {"hello": "greeting", "how much does the course cost": "pricing",
                 "i want a refund": "refund", "what time is it": "time",
                 "do you offer internships": "internship", "thank you": "thanks"}
        for text, expected in cases.items():
            self.assertEqual(self.intent(text), expected, text)

    def test_out_of_scope_goes_to_fallback(self):
        self.assertEqual(self.intent("asdf qwerty zxcv"), "fallback")

    def test_remembers_name(self):
        state = {}
        self.bot.respond("my name is Ravi", state)
        self.assertEqual(state["name"], "Ravi")
        self.assertIn("Ravi", self.bot.respond("bye", state)["reply"])

    def test_empty_message(self):
        self.assertEqual(self.bot.respond("   ")["intent"], "empty")

    def test_time_reply_is_dynamic(self):
        self.assertRegex(self.bot.respond("what time is it", {})["reply"], r"\d{1,2}:\d{2}")


if __name__ == "__main__":
    unittest.main()
