import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk, ImageSequence
import threading
import os
import time
from chatbot_logic import get_bot_response
from mood_detector import detect_mood
from sprite_manager import load_sprite_variants, get_sprite_for_mood
from threading import Event
import pygame
import random
import requests
from path_utils import get_asset_path

# === Initialize sound ===
pygame.mixer.init()

# === File paths ===
base_path = os.path.dirname(os.path.abspath(__file__))

# Load sound effects
try:
    typing_sound = pygame.mixer.Sound(get_asset_path("assets/sfx/typing sound.wav"))
    typing_sound.set_volume(0.3)
except Exception as e:
    with open("log.txt", "a") as f:
        f.write("[SOUND ERROR] " + str(e) + "\n")
    typing_sound = None

background_music = pygame.mixer.Sound(get_asset_path("assets/sfx/background music.wav"))
background_music.set_volume(0.1)
background_music.play(loops=-1)

# === Globals ===
typing_done = Event()
skip_typewriter = False
sprite_animation_job = None

# === Sprite dictionaries ===
sprite_dict = load_sprite_variants()

special_sprites = {
    "welcome": get_asset_path("assets/sprites/talking.gif"),
    "loading": get_asset_path("assets/sprites/loading.gif"),
    "error": get_asset_path("assets/sprites/error.png"),
    "talking": get_asset_path("assets/sprites/talking.gif")
}

rps_sprites = {
    "rock": get_asset_path("assets/sprites/rps_rock.png"),
    "paper": get_asset_path("assets/sprites/rps_paper.png"),
    "scissors": get_asset_path("assets/sprites/rps_scissors.png")
}

weather_sprites = {
    "Clear": get_asset_path("assets/sprites/sunny.gif"),
    "Clouds": get_asset_path("assets/sprites/cloudy.gif"),
    "Rain": get_asset_path("assets/sprites/rainy.gif"),
    "Drizzle": get_asset_path("assets/sprites/rainy.gif"),
    "Thunderstorm": get_asset_path("assets/sprites/rainy.gif"),
    "Snow": get_asset_path("assets/sprites/cloudy.gif"),
    "Fog": get_asset_path("assets/sprites/cloudy.gif"),
    "Windy": get_asset_path("assets/sprites/windy.gif")
}

# === JoJo mode setup ===
jojo_keywords = [
    "jojo", "jojos", "jotaro", "dio", "kira", "josuke", "giorno", "bruno", "polnareff", "caesar", "lisa lisa",
    "speedwagon", "hol horse", "okuyasu", "mista", "abbacchio", "diavolo", "pucci", "jolyne", "anastasia",
    "ermes", "gyro", "valentine", "gappy", "yasuho", "stand", "muda", "za warudo", "yare yare daze",
    "kono dio da", "requiem", "king crimson", "gold experience", "killer queen", "bites the dust",
    "soft & wet", "crazy diamond", "star platinum", "stone ocean", "heaven's door"
]

jojo_sprites = [
    get_asset_path("assets/sprites/jojo1.png"),
    get_asset_path("assets/sprites/jojo2.png"),
    get_asset_path("assets/sprites/jojo3.png")
]

# === Tkinter UI Setup ===
root = tk.Tk()
root.title("🤖MacnCheese™")
root.configure(bg='#1e1e1e')

# === Layout: Chat interface ===
chat_frame = tk.Frame(root, bg='#1e1e1e')
chat_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

chat_display = tk.Text(
    chat_frame, height=25, width=60, bg='#1e1e1e', fg='#00FF7F',
    font=("Consolas", 12), state='disabled', wrap='word', bd=0
)
chat_display.pack()

entry_frame = tk.Frame(chat_frame, bg='#1e1e1e')
entry_frame.pack(pady=5)

user_entry = tk.Entry(
    entry_frame, width=45, font=("Consolas", 12), bg='#2e2e2e',
    fg='#00FF7F', insertbackground='#00FF7F', bd=1
)
user_entry.grid(row=0, column=0, padx=(0, 5))

# === Layout: Sprite and button interface ===
sprite_frame = tk.Frame(root, bg='#1e1e1e')
sprite_frame.grid(row=0, column=1, padx=10, pady=10)

sprite_label = tk.Label(sprite_frame, bg='#1e1e1e')
sprite_label.pack()

rps_area = tk.Frame(sprite_frame, bg="#1e1e1e")
rps_area.pack(pady=(10, 0))

button_frame = tk.Frame(sprite_frame, bg='#1e1e1e')
button_frame.pack(pady=10)

# === Buttons: Weather and Rock Paper Scissors ===
weather_button = tk.Button(
    button_frame, text="Check Weather", bg='#333', fg='#00FF7F',
    font=("Consolas", 10), command=lambda: typewriter_effect("MacnCheese", get_weather_response())
)
weather_button.grid(row=0, column=0, padx=5)

rps_button = tk.Button(
    button_frame, text="Rock Paper Scissors", bg='#333', fg='#00FF7F',
    font=("Consolas", 10), command=lambda: start_rps_game()
)
rps_button.grid(row=0, column=1, padx=5)

# === Animation system for sprite display ===
frames = []
frame_index = 0

def show_sprite(sprite_path):
    global frames, frame_index, sprite_animation_job
    print(f"[DEBUG] show_sprite called with: {sprite_path}")

    # Cancel previous animation if it exists
    if sprite_animation_job is not None:
        try:
            sprite_label.after_cancel(sprite_animation_job)
        except Exception as e:
            print(f"[DEBUG] Tried to cancel animation but got: {e}")
        sprite_animation_job = None

    img = Image.open(sprite_path)

    if getattr(img, "is_animated", False):
        # Handle animated GIFs
        frames = [ImageTk.PhotoImage(frame.copy().resize((256, 256))) for frame in ImageSequence.Iterator(img)]
        frame_index = 0

        def update_frame():
            global frame_index, sprite_animation_job
            sprite_label.config(image=frames[frame_index])
            sprite_label.image = frames[frame_index]
            frame_index = (frame_index + 1) % len(frames)
            sprite_animation_job = sprite_label.after(300, update_frame)

        update_frame()
    else:
        # Handle static images
        img = img.resize((256, 256))
        tk_img = ImageTk.PhotoImage(img)
        sprite_label.config(image=tk_img)
        sprite_label.image = tk_img
        sprite_animation_job = None

# === Display a message in the chat window ===
def append_message(sender, message):
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, f"{sender}: {message}\n")
    chat_display.configure(state='disabled')
    chat_display.see(tk.END)

# === Animate bot text one character at a time ===
def typewriter_effect(sender, message, delay=25, callback=None):
    global skip_typewriter
    skip_typewriter = False

    chat_display.configure(state='normal')
    chat_display.insert(tk.END, f"{sender}: ")
    chat_display.configure(state='disabled')
    chat_display.see(tk.END)

    if sender.lower() == "bot":
        typing_done.clear()
        if typing_sound:
            typing_sound.play(loops=-1)
        else:
            with open("log.txt", "a") as f:
                f.write("[WARNING] Typing sound was not loaded — skipping play()\n")

    def type_char(index=0):
        global skip_typewriter

        if skip_typewriter:
            # Skip animation and show full message
            chat_display.configure(state='normal')
            chat_display.insert(tk.END, message[index:] + "\n")
            chat_display.configure(state='disabled')
            chat_display.see(tk.END)
            typing_sound.stop()
            typing_done.set()
            if callback:
                callback()
            return

        if index < len(message):
            chat_display.configure(state='normal')
            chat_display.insert(tk.END, message[index])
            chat_display.configure(state='disabled')
            chat_display.see(tk.END)
            root.after(delay, type_char, index + 1)
        else:
            typing_sound.stop()
            typing_done.set()
            chat_display.configure(state='normal')
            chat_display.insert(tk.END, "\n")
            chat_display.configure(state='disabled')
            if callback:
                callback()

    root.after(delay, type_char)

# === Handle user input from chat box ===
def process_input():
    user_input = user_entry.get().strip()
    print(f"[DEBUG] process_input: {user_input}")
    user_entry.delete(0, tk.END)

    if not user_input:
        return

    # Handle exit command
    if user_input.lower() in ["exit", "quit"]:
        append_message("You", user_input)
        print("[DEBUG] User requested exit")

        def exit_callback():
            typing_sound.stop()
            background_music.stop()
            print("[DEBUG] Shutting down app")
            root.after(2000, root.destroy)

        typewriter_effect("Bot", "Goodbye! Thanks for chatting !", callback=exit_callback)
        return

    # Display user input
    append_message("You", user_input)
    show_sprite(special_sprites["loading"])

    # Prepare background thread to generate bot reply
    response_ready = Event()
    response_data = {}

    def worker():
        try:
            print("[DEBUG] get_bot_response called with:", user_input)
            response = get_bot_response(user_input)
            print("[DEBUG] Gemini raw response:", response)

            # JoJo keyword check has priority
            if any(word in user_input.lower() for word in jojo_keywords):
                sprite_path = random.choice(jojo_sprites)
                print("[DEBUG] JoJo keyword detected — using special sprite")
            else:
                mood = detect_mood(user_input)
                sprite_path = get_sprite_for_mood(mood, sprite_dict) or special_sprites["talking"]
                print("[DEBUG] Mood detected:", mood)

            response_data.update({
                "response": response,
                "sprite_path": sprite_path
            })
        except Exception as e:
            print("[DEBUG] Gemini Error:", e)
            response_data["error"] = e
        finally:
            response_ready.set()

    threading.Thread(target=worker, daemon=True).start()

    # Poll until worker thread completes or times out
    def check_response():
        if response_ready.is_set() or (time.time() - start_time > 3):
            if "error" in response_data:
                append_message("Bot", "[Oops, something went wrong!]")
                print("[ERROR]", response_data["error"])
                show_sprite(special_sprites["error"])
                return

            sprite_path = response_data.get("sprite_path", special_sprites["welcome"])
            response = response_data.get("response", "[No response]")
            show_sprite(sprite_path)

            def after_typewriter():
                print("[DEBUG] Typewriter finished")

            typewriter_effect("Bot", response, callback=after_typewriter)
        else:
            root.after(100, check_response)

    start_time = time.time()
    root.after(100, check_response)

# === Send button for manual input ===
send_button = tk.Button(
    entry_frame, text="Send", command=process_input,
    bg='#333', fg='#00FF7F', font=("Consolas", 12)
)
send_button.grid(row=0, column=1)

# === Handle Enter key for sending or skipping typewriter ===
def on_enter_key(event=None):
    global skip_typewriter
    if not typing_done.is_set():
        skip_typewriter = True
    else:
        process_input()

user_entry.bind("<Return>", on_enter_key)

# === Startup welcome message ===
def show_welcome_message():
    show_sprite(special_sprites["welcome"])
    typewriter_effect("Bot", (
        "Hello there! My name is MacnCheese and I have been created by Harshit\n\n"
        "Anyways! I am here to be your BEST FRIEND! WOOO  excited? I would be if I were you!\n\n"
        "You can freely talk to me and I will answer back to you till best of my knowledge.\n\n"
        "If you want to stop talking to me ( please don't leave ) just type 'quit' or 'exit'. And if you want to skip the characters animations just hit Enter in the chatbox! Easy peasy!\n\n"
        "Let's start this conversation! How are you feeling today?"
    ))

# === Weather API call and sprite display ===
def get_weather_response(lat=28.6139, lon=-77.2090):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )
        data = requests.get(url, timeout=5).json()
        cw = data.get("current_weather", {})
        temp = cw.get("temperature")
        wind = cw.get("windspeed")
        code = cw.get("weathercode")

        # Weather code mapping
        mapping = {
            0: "Clear", 1: "Clouds", 2: "Clouds", 3: "Clouds",
            45: "Fog", 48: "Fog",
            51: "Drizzle", 53: "Drizzle", 55: "Drizzle",
            61: "Rain", 63: "Rain", 65: "Rain",
            71: "Snow", 73: "Snow", 75: "Snow",
            80: "Rain", 81: "Rain", 82: "Rain",
            95: "Thunderstorm"
        }
        cat = mapping.get(code, "Clear")
        show_sprite(weather_sprites.get(cat, special_sprites["talking"]))

        return f"It's {temp}°C in delhi with wind at {wind} km/h—looks like {cat.lower()}!"
    except Exception as e:
        print("[Weather Error]", e)
        return "[Weather service unavailable right now.]"

# === Get sprite for RPS choice ===
def get_rps_sprite(choice):
    return rps_sprites.get(choice, special_sprites["talking"])

# === Start Rock Paper Scissors game ===
def start_rps_game():
    for widget in rps_area.winfo_children():
        widget.destroy()

    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)

    def on_choice(user_choice):
        for widget in rps_area.winfo_children():
            widget.destroy()

        sprite_path = get_rps_sprite(bot_choice)
        show_sprite(sprite_path)

        if user_choice == bot_choice:
            result = f"It's a tie! MacnCheese also chose {bot_choice}."
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            result = f"You win! MacnCheese chose {bot_choice}."
        else:
            result = f"You lose! MacnCheese chose {bot_choice}."

        typewriter_effect("MacnCheese", result)

    # Show option buttons under mascot
    for i, option in enumerate(choices):
        tk.Button(
            rps_area,
            text=option.title(),
            width=12,
            command=lambda c=option: on_choice(c),
            bg="#333",
            fg="#00FF7F",
            font=("Consolas", 10)
        ).grid(row=0, column=i, padx=5, pady=5)

# === Configure window to expand properly ===
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# === Launch welcome message on startup ===
root.after(300, show_welcome_message)

# === Start the main event loop ===
root.mainloop()