"""Train + evaluate the chatbot, and write a sample conversation.

    python main.py
"""
from src import config as cfg
from src.chatbot import Chatbot
from src.train import run_training

SAMPLE = ["hello", "my name is Asha", "what courses do you offer", "how much does it cost",
          "i want a refund", "do you give internships", "what time is it", "tell me a joke",
          "what is machine learning", "how do i cook pasta", "thanks", "bye"]


def main():
    print("[1/3] Training and comparing models ...")
    comp, metrics, errors = run_training()
    print(comp.to_string(index=False))

    print(f"\n[2/3] Chosen model: {metrics['chosen_model']}")
    for k, v in metrics["external_test"].items():
        print(f"      {k:24s} {v}")
    print(f"      misclassified queries saved: {len(errors)}")

    print("\n[3/3] Sample conversation")
    bot, state, md = Chatbot(seed=1), {}, ["# Sample conversation\n"]
    for msg in SAMPLE:
        r = bot.respond(msg, state)
        print(f"  You : {msg}\n  Bot : {r['reply']}   [{r['intent']}, {r['confidence']}]")
        md += [f"**You:** {msg}  ", f"**Cogni:** {r['reply']}  ", f"*(intent: `{r['intent']}`, confidence {r['confidence']})*\n"]
    (cfg.OUTPUT_DIR / "sample_conversation.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\nDone. See {cfg.OUTPUT_DIR}/ and run `python app.py` for the web UI.")


if __name__ == "__main__":
    main()
