# Project Report – AI Chatbot using NLP

**Name:** <your name>  **Date:** <date>  **Programme:** Cognevance Technologies – AI & ML, Level 2

## 1. Objective
Build an intelligent chatbot that understands user queries with NLP, recognises their intent and
generates a suitable response, with a simple user interface and a measured accuracy.

## 2. Data
- **Training data:** `data/intents.json`, written by hand: 27 intents (greetings, courses, fees,
  enrollment, refunds, certificates, internships, support, time/date, jokes, AI info, small talk and an
  out-of-scope class) with 392 example sentences in total, 12 to 17 per intent (the out-of-scope class has 35).
- **Test data:** `data/test_queries.csv`, 114 separate hand-written queries (104 in-scope paraphrases and
  10 out-of-scope questions). None of them is copied from the training patterns.

## 3. NLP preprocessing (`src/preprocess.py`)
1. Lower-casing and collapsing repeated letters ("heyyyy" → "heyy").
2. Expanding contractions and slang ("what's" → "what is", "thx" → "thanks", "u" → "you").
3. Tokenising with a regular expression (letters and digits only).
4. Removing a small list of filler words (question words and pronouns are kept because they carry intent).
5. Stemming with NLTK's Porter stemmer ("courses" → "cours", "enrolling" → "enrol").

## 4. Model
Text is converted to TF-IDF features (unigrams + bigrams) and classified. Three classifiers were compared:
Logistic Regression, Linear SVM (probability-calibrated) and Naive Bayes. Logistic Regression was chosen
because it had the best cross-validated accuracy and gives the probability estimates that the confidence
threshold needs.

**Response generation:** a random response from the predicted intent's list. `{time}`, `{date}` and the
user's name are filled in at run time. If the top probability is below 0.20 the bot answers with a fallback
message.

**Interface:** Flask web app (`app.py`, `templates/index.html`) and a terminal chat (`chat_cli.py`).

## 5. Results

| Model | 5-fold CV accuracy | Hold-out accuracy | External test accuracy | External macro F1 |
|---|---|---|---|---|
| Logistic Regression | 0.622 | 0.620 | **0.974** | 0.978 |
| Linear SVM (calibrated) | 0.620 | 0.646 | 0.947 | 0.951 |
| Naive Bayes | 0.597 | 0.633 | 0.939 | 0.945 |

Chosen model on the external test set: accuracy 97.4 %, macro F1 0.978, in-scope accuracy 99.0 %,
out-of-scope questions rejected 80 %. Only 3 of 114 queries were wrong (`outputs/misclassified_queries.csv`):
"are you a robot" was read as small talk, and "what is the price of bitcoin" and "how do i cook pasta"
were answered as if they were about our courses.

Charts: `outputs/figures/01_model_comparison.png`, `02_confusion_matrix.png`, `03_threshold_sweep.png`.

### Improving the bot (iteration)
- First version (no out-of-scope class, about 300 examples): 86 % external accuracy, and unrelated
  questions such as "who won the football match yesterday" got confident but wrong answers.
- Fixes: added an explicit out-of-scope class and about 90 more examples, then lowered the
  confidence threshold from 0.30 to 0.20 after looking at the threshold sweep.
- Result: external accuracy rose from 86 % to 97 %.

## 6. Limitations (please read)
- **Cross-validation accuracy is only about 62 %.** Each intent has only 12 to 17 examples, so when 20 % are
  held out the model sees very few examples of the intent. The external test set scores much higher because
  its queries share more wording with the training patterns. The true accuracy on real users' messages will
  be lower than 97 %.
- The test set is small (114 queries) and written by the same author as the training data. Some extra
  training examples were added after reading the first error list, so the 97 % figure is somewhat optimistic.
  The threshold of 0.20 was also chosen using this test set.
- The bot matches intents; it does not generate free-form text, keep multi-turn context (except the user's
  name) or look up live data (weather is declined on purpose).
- Business details in the responses (fees, refund window, hours, email) are placeholders to be replaced.

## 7. Conclusion
A TF-IDF + Logistic Regression intent classifier with careful preprocessing gives a working chatbot that
answers its supported topics well and refuses most unrelated questions. Next steps: collect real user
messages for training, add multi-turn context, and try a transformer-based sentence encoder.

## 8. How to run
See `README.md`.
