"""Paths and hyper-parameters in one place."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
INTENTS_PATH = DATA_DIR / "intents.json"        # training data (patterns + responses)
TEST_PATH = DATA_DIR / "test_queries.csv"       # separate, hand-written evaluation set

MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "intent_model.joblib"

OUTPUT_DIR = ROOT / "outputs"
FIG_DIR = OUTPUT_DIR / "figures"

RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# If the model's top probability is below this, the bot says "I didn't understand".
CONFIDENCE_THRESHOLD = 0.20
FALLBACK_INTENT = "fallback"
BOT_NAME = "Cogni"
