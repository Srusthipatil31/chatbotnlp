"""Train, compare and save the intent-classification model."""
import json

import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from src import config as cfg
from src.evaluate import (external_report, save_confusion_matrix, save_model_comparison_chart,
                          save_threshold_chart, threshold_sweep)
from src.preprocess import STEMMER, preprocess


def load_training_data() -> pd.DataFrame:
    data = json.loads(cfg.INTENTS_PATH.read_text(encoding="utf-8"))
    rows = [(p, i["tag"]) for i in data["intents"] for p in i["patterns"]]
    return pd.DataFrame(rows, columns=["text", "intent"])


def make_pipeline(classifier) -> Pipeline:
    vec = TfidfVectorizer(preprocessor=preprocess, token_pattern=r"\S+", ngram_range=(1, 2),
                          sublinear_tf=True)
    return Pipeline([("tfidf", vec), ("clf", classifier)])


def candidate_models() -> dict:
    return {
        "Logistic Regression": make_pipeline(LogisticRegression(C=20, max_iter=2000)),
        "Linear SVM (calibrated)": make_pipeline(CalibratedClassifierCV(LinearSVC(C=1.0), cv=3)),
        "Naive Bayes": make_pipeline(MultinomialNB(alpha=0.1)),
    }


def run_training(verbose=True):
    cfg.MODEL_DIR.mkdir(exist_ok=True)
    cfg.FIG_DIR.mkdir(parents=True, exist_ok=True)

    df = load_training_data()
    test_df = pd.read_csv(cfg.TEST_PATH)
    if verbose:
        print(f"      training patterns: {len(df)} | intents: {df['intent'].nunique()} | "
              f"external test queries: {len(test_df)} | stemmer: {STEMMER}")

    # ---- 1. compare models --------------------------------------------------
    X_tr, X_te, y_tr, y_te = train_test_split(df["text"], df["intent"], test_size=cfg.TEST_SIZE,
                                              stratify=df["intent"], random_state=cfg.RANDOM_STATE)
    cv = StratifiedKFold(n_splits=cfg.CV_FOLDS, shuffle=True, random_state=cfg.RANDOM_STATE)
    rows = []
    for name, pipe in candidate_models().items():
        cv_acc = cross_val_score(pipe, df["text"], df["intent"], cv=cv, scoring="accuracy").mean()
        pipe.fit(X_tr, y_tr)
        split_pred = pipe.predict(X_te)
        pipe.fit(df["text"], df["intent"])                      # fit on all patterns for external test
        ext, _, _ = external_report(pipe, test_df, threshold=cfg.CONFIDENCE_THRESHOLD)
        rows.append({"model": name,
                     "cv_accuracy": round(cv_acc, 4),
                     "holdout_accuracy": round(accuracy_score(y_te, split_pred), 4),
                     "holdout_macro_f1": round(f1_score(y_te, split_pred, average="macro"), 4),
                     "external_accuracy": ext["accuracy"],
                     "external_in_scope_accuracy": ext["in_scope_accuracy"],
                     "external_macro_f1": ext["macro_f1"]})
    comp = pd.DataFrame(rows)
    comp.to_csv(cfg.OUTPUT_DIR / "model_comparison.csv", index=False)
    save_model_comparison_chart(comp, cfg.FIG_DIR / "01_model_comparison.png")

    # ---- 2. pick the best model (by cross-validated accuracy) ----------------
    best_name = comp.sort_values(["cv_accuracy", "external_accuracy"], ascending=False).iloc[0]["model"]
    best = candidate_models()[best_name].fit(df["text"], df["intent"])
    joblib.dump(best, cfg.MODEL_PATH)

    # ---- 3. detailed evaluation of the chosen model ---------------------------
    ext, pred, errors = external_report(best, test_df, cfg.CONFIDENCE_THRESHOLD)
    errors.to_csv(cfg.OUTPUT_DIR / "misclassified_queries.csv", index=False)
    sweep = threshold_sweep(best, test_df["text"].tolist(), test_df["intent"].values)
    sweep.to_csv(cfg.OUTPUT_DIR / "threshold_sweep.csv", index=False)
    save_threshold_chart(sweep, cfg.FIG_DIR / "03_threshold_sweep.png")
    save_confusion_matrix(test_df["intent"].values, pred, cfg.FIG_DIR / "02_confusion_matrix.png",
                          f"Confusion matrix – {best_name} (external test set)")
    report = classification_report(test_df["intent"], pred, output_dict=True, zero_division=0)
    pd.DataFrame(report).T.round(3).to_csv(cfg.OUTPUT_DIR / "classification_report.csv")

    metrics = {"chosen_model": best_name, "confidence_threshold": cfg.CONFIDENCE_THRESHOLD,
               "n_training_patterns": int(len(df)), "n_intents": int(df["intent"].nunique()),
               "external_test": ext}
    (cfg.OUTPUT_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return comp, metrics, errors
