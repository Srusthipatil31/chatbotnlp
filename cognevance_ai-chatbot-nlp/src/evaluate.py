"""Evaluation helpers: metrics, confusion matrix, error analysis."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, classification_report,
                             confusion_matrix, f1_score)

from src import config as cfg


def predict_with_threshold(model, texts, threshold):
    probs = model.predict_proba(texts)
    idx = probs.argmax(axis=1)
    conf = probs.max(axis=1)
    labels = model.classes_[idx].astype(object)
    labels[conf < threshold] = cfg.FALLBACK_INTENT
    return labels, conf


def threshold_sweep(model, texts, y_true, thresholds=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)):
    rows = []
    for t in thresholds:
        pred, _ = predict_with_threshold(model, texts, t)
        rows.append({"threshold": t,
                     "accuracy": round(accuracy_score(y_true, pred), 4),
                     "macro_f1": round(f1_score(y_true, pred, average="macro", zero_division=0), 4)})
    return pd.DataFrame(rows)


def external_report(model, test_df, threshold):
    pred, conf = predict_with_threshold(model, test_df["text"].tolist(), threshold)
    y = test_df["intent"].values
    in_scope = y != cfg.FALLBACK_INTENT
    result = {
        "n_queries": int(len(y)),
        "accuracy": round(float(accuracy_score(y, pred)), 4),
        "macro_f1": round(float(f1_score(y, pred, average="macro", zero_division=0)), 4),
        "in_scope_accuracy": round(float(accuracy_score(y[in_scope], pred[in_scope])), 4),
        "out_of_scope_rejected": round(float((pred[~in_scope] == cfg.FALLBACK_INTENT).mean()), 4),
    }
    errors = test_df.assign(predicted=pred, confidence=conf.round(3))
    errors = errors[errors["intent"] != errors["predicted"]]
    return result, pred, errors


def save_confusion_matrix(y_true, y_pred, path, title):
    labels = sorted(set(y_true) | set(y_pred))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(13, 11))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="Blues", colorbar=False,
                                                           xticks_rotation=75, values_format="d")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def save_model_comparison_chart(comp_df, path):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(comp_df))
    ax.bar(x - 0.2, comp_df["cv_accuracy"], 0.4, label="5-fold CV accuracy", color="#2f6fb7")
    ax.bar(x + 0.2, comp_df["external_accuracy"], 0.4, label="External test accuracy", color="#e07b39")
    ax.set_xticks(x)
    ax.set_xticklabels(comp_df["model"], rotation=15)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Accuracy")
    ax.set_title("Intent classifier comparison")
    ax.legend(loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def save_threshold_chart(sweep_df, path):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sweep_df["threshold"], sweep_df["accuracy"], marker="o", label="Accuracy")
    ax.plot(sweep_df["threshold"], sweep_df["macro_f1"], marker="s", label="Macro F1")
    ax.axvline(cfg.CONFIDENCE_THRESHOLD, ls="--", color="grey", label="chosen threshold")
    ax.set_xlabel("Confidence threshold for 'fallback'")
    ax.set_ylabel("Score on external test set")
    ax.set_title("Effect of the fallback threshold")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
