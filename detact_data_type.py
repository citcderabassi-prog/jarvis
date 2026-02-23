import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

training_data = [
    # Knowledge
    ("what is python", "knowledge"),
    ("who is elon musk", "knowledge"),
    ("define gravity", "knowledge"),
    ("explain ai", "knowledge"),
    ("what is happening with the india-france defence talks", "knowledge"),
    ("what is the news about india france defence", "knowledge"),
    ("what is happening with the news today", "knowledge"),
    ("give me current news", "knowledge"),



    # Real-time
    ("weather today", "real_time"),
    ("current bitcoin price", "real_time"),
    ("live cricket score", "real_time"),
    ("current bitcoin price", "real_time"),
    ("live bitcoin price", "real_time"),
    ("bitcoin price now", "real_time"),
    ("what is bitcoin price", "real_time"),
    ("what is live price of bitcoin", "real_time"),
    ("btc price today", "real_time"),
    ("bitcoin rate now", "real_time"),
    ("what is the price of bitcoin right now", "real_time"),
    ("You: Tell me the latest news.","real_time"),
    ("latest news of india ai","real_time"),
    # Chat

    ("hi", "chat"),
    ("hello", "chat"),
    ("hey", "chat"),
    ("hey there", "chat"),
    ("good morning", "chat"),
    ("good afternoon", "chat"),
    ("good evening", "chat"),
    ("what's up", "chat"),
    ("how's it going", "chat"),
    ("what can you do", "chat"),
    ("What is your purpose", "chat"),
    ("What is the time", "chat"),
    ("What day is today","chat"),


    # Automation
    ("open chrome", "automation"),
    ("shutdown system", "automation"),
    ("play music", "automation"),
    ("restart computer", "automation"),
    ("open chrome", "automation"),
    ("can you open youtube", "automation"),
    ("open notepad", "automation"),
    ("open calculator", "automation"),
    ("start spotify", "automation"),
    ("close chrome", "automation"),
    ("restart computer", "automation"),
    ("shutdown pc", "automation"),
    # Math
    ("2 + 2", "math"),
    ("10 / 5", "math"),

    # Memory
    ("remember my name is john", "memory"),
    ("what is my name", "memory"),


]
# Training data (expand this a LOT in real usage)


X = [text for text, label in training_data]
y = [label for text, label in training_data]

# Build ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

model.fit(X, y)

# Save model
joblib.dump(model, "intent_model.pkl")

print("Model trained and saved.")

import joblib

model = joblib.load("intent_model.pkl")

def detect_intent(query):
    prediction = model.predict([query])[0]
    confidence = max(model.predict_proba([query])[0])
    return prediction, confidence
# while True:
#     intent, confidence = detect_intent(input("> "))
#     print("Intent : ", intent)
#     print("Confidence : ", confidence)



