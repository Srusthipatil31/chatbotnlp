"""Text preprocessing (the NLP step).

Pipeline:  lower-case -> expand contractions/slang -> keep letters & digits ->
           tokenise -> drop a few filler words -> stem (NLTK PorterStemmer)

NLTK's PorterStemmer needs no extra downloads. If NLTK isn't installed, a tiny
built-in suffix stemmer is used so the project still runs.
"""
import re

try:
    from nltk.stem.porter import PorterStemmer
    _PORTER = PorterStemmer()
    STEMMER = "nltk.PorterStemmer"
except Exception:                    # pragma: no cover - only when nltk is missing
    _PORTER = None
    STEMMER = "built-in fallback stemmer"

CONTRACTIONS = {
    "what's": "what is", "whats": "what is", "that's": "that is", "it's": "it is", "how's": "how is",
    "i'm": "i am", "im": "i am", "you're": "you are", "i've": "i have", "i'd": "i would",
    "don't": "do not", "dont": "do not", "can't": "can not", "cant": "can not", "won't": "will not",
    "didn't": "did not", "doesn't": "does not", "isn't": "is not", "let's": "let us", "today's": "today",
}
SLANG = {"thx": "thanks", "pls": "please", "plz": "please", "u": "you", "ur": "your", "r": "are",
         "hii": "hi", "hiii": "hi", "hey": "hello", "yo": "hello", "bye": "goodbye", "ok": "okay"}
# Only filler words are removed: question words and pronouns carry meaning for intents.
STOPWORDS = {"a", "an", "the", "is", "are", "am", "was", "were", "be", "to", "of", "it", "its",
             "this", "that", "please", "me", "my"}


def _fallback_stem(word: str) -> str:
    for suffix in ("ing", "ed", "es", "s", "ly"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def stem(word: str) -> str:
    return _PORTER.stem(word) if _PORTER else _fallback_stem(word)


def tokenize(text: str) -> list:
    text = text.lower().strip()
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)          # "heyyyy" -> "heyy"
    text = text.replace("’", "'")
    for short, full in CONTRACTIONS.items():
        text = re.sub(rf"\b{re.escape(short)}\b", full, text)
    return re.findall(r"[a-z0-9]+", text)


def preprocess(text: str) -> str:
    """Raw sentence -> cleaned, stemmed string used by the TF-IDF vectoriser."""
    tokens = [SLANG.get(t, t) for t in tokenize(text)]
    tokens = [t for t in tokens if t not in STOPWORDS]
    return " ".join(stem(t) for t in tokens)


if __name__ == "__main__":
    for s in ["Hiii!! What's the TIME right now?", "I don't think so", "thx for the help pls"]:
        print(f"{s!r:40} -> {preprocess(s)!r}")
