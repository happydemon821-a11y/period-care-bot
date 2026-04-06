import tkinter as tk
from PIL import Image, ImageTk
import random
import speech_recognition as sr
import pyttsx3
from datetime import datetime, timedelta
import json
import os

# ---------- VOICE ----------
engine = pyttsx3.init()

def speak(text):
    chat_log.insert(tk.END, "Bot: " + text + "\n")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        chat_log.insert(tk.END, "🎤 Listening...\n")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        chat_log.insert(tk.END, "You: " + text + "\n")
        return text.lower()
    except:
        return ""

# ---------- DATA ----------
DATA_FILE = "period_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

user_data = load_data()

# ---------- PERIOD TRACK ----------
def set_period():
    date = entry.get()
    try:
        datetime.strptime(date, "%d-%m-%Y")
        user_data["last_period"] = date
        user_data["cycle"] = 28
        save_data(user_data)
        speak("Period data saved")
    except:
        speak("Enter date in DD-MM-YYYY format")

def predict_period():
    if "last_period" not in user_data:
        speak("Please set period first")
        return

    last = datetime.strptime(user_data["last_period"], "%d-%m-%Y")
    next_date = last + timedelta(days=user_data.get("cycle", 28))
    speak(f"Next period: {next_date.strftime('%d %B %Y')}")

# ---------- IMAGE IN CHAT ----------
def show_image(img_path, text):
    try:
        img = Image.open(img_path).resize((120, 120))
        img = ImageTk.PhotoImage(img)

        chat_log.insert(tk.END, "Bot: " + text + "\n")
        chat_log.image_create(tk.END, image=img)
        chat_log.insert(tk.END, "\n\n")

        if not hasattr(chat_log, "images"):
            chat_log.images = []
        chat_log.images.append(img)

    except:
        chat_log.insert(tk.END, "Image not found\n")

# ---------- SMART AI ----------
import difflib

def match_intent(user, keywords):
    words = user.split()
    for word in words:
        match = difflib.get_close_matches(word, keywords, n=1, cutoff=0.6)
        if match:
            return True
    return False
def smart_reply(user):
    user = user.lower()

    pain_words = ["pain", "cramp", "hurt", "stomach", "ache"]
    food_words = ["food", "eat", "diet", "drink"]
    exercise_words = ["exercise", "yoga", "workout", "stretch"]
    mood_words = ["sad", "tired", "angry", "emotional", "mood"]

    # 🍎 FOOD
    if match_intent(user, food_words):
        show_image("banana.png", "Banana 🍌 helps reduce cramps")
        show_image("chocolate.png", "Dark chocolate 🍫 helps relax muscles")
        show_image("ginger_tea.png", "Ginger tea 🍵 reduces pain")
        return "These foods can help you 💜"

    # 🧘 EXERCISE
    elif match_intent(user, exercise_words):
        show_image("child_pose.png", "Child’s Pose 🧘‍♀️ relaxes muscles")
        show_image("cat_cow.png", "Cat-Cow stretch improves flexibility")
        return "Try these exercises 🧘‍♀️"

    # 💢 PAIN
    elif match_intent(user, pain_words):
        return random.choice([
            "Use heating pad 🔥 and take rest.",
            "Try gentle yoga to relax muscles.",
            "Drink warm fluids like ginger tea ☕"
        ])

    # 💜 MOOD
    elif match_intent(user, mood_words):
        return random.choice([
            "It's okay 💜 Take care of yourself.",
            "Rest and relax, you're doing fine 😊",
            "Be kind to yourself today 💕"
        ])

    # 📅 TRACK
    elif "track" in user:
        return "Enter your last period date and click Save Period."

    elif "predict" in user:
        predict_period()
        return ""

    # 👋 GREETING
    elif match_intent(user, ["hello", "hi", "hey"]):
        return "Hi 💜 I'm here for you."

    # 🤖 DEFAULT
    else:
        return random.choice([
            "I understand 💜 Tell me more.",
            "I'm here to help 😊",
            "You can ask about pain, food, exercise, or mood."
        ])
# ---------- CHAT ----------
def send_text():
    user = entry.get()
    chat_log.insert(tk.END, "You: " + user + "\n")
    entry.delete(0, tk.END)

    response = smart_reply(user)
    if response:
        speak(response)

def voice_input():
    user = listen()
    if user:
        response = smart_reply(user)
        if response:
            speak(response)

# ---------- UI ----------
root = tk.Tk()
root.title("Period Care AI")
root.geometry("500x650")

chat_log = tk.Text(root, height=20, width=60, wrap="word")
chat_log.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Send", command=send_text).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="🎤 Speak", command=voice_input).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Save Period", command=set_period).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Predict", command=predict_period).grid(row=0, column=3, padx=5)

root.mainloop()