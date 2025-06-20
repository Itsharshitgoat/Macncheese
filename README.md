# MacnCheese Chat Bot

A highly interactive, personality-rich desktop chatbot built with Python, Tkinter, and the Gemini API. MacnCheese features animated sprites, mood detection, sound effects, weather info, and even a Rock-Paper-Scissors minigame—all wrapped in a fun, pixel-art interface.

---

## Features

- **Conversational AI**: Uses Google Gemini API for natural, witty, and context-aware responses.
- **Mood Detection**: Analyzes user input with VADER sentiment analysis and custom keyword matching to select expressive sprites.
- **Animated Sprites**: Displays pixel-art GIFs and PNGs that change based on mood, special events, or minigames.
- **Sound Effects & Music**: Plays typing sounds and looping background music for an immersive experience.
- **Weather Integration**: Fetches and displays current weather with matching animated sprites.
- **Rock-Paper-Scissors Game**: Play a quick game with the bot, complete with custom sprites.
- **JoJo Mode**: Detects JoJo’s Bizarre Adventure references and swaps in special themed sprites.
- **Robust Error Handling**: Logs errors and API issues to `log.txt` for easy debugging.
- **Asset Bundling Support**: Handles asset paths for both development and PyInstaller-bundled executables.

---

## File Structure

```
Chat Bot/
├── assets/
│   ├── sprites/           # All PNG/GIF sprite assets (mood, special, RPS, JoJo, etc.)
│   └── sfx/               # Sound effects and background music
├── chatbot_logic.py       # Handles prompt cleaning, Gemini API, and bot response logic
├── macncheese.py          # Main Tkinter GUI, event loop, sprite/sound/game logic
├── mood_detector.py       # Mood detection using VADER and custom keywords
├── path_utils.py          # Asset path resolution for dev and bundled modes
├── prompt_utils.py        # Prompt cleaning and personality injection
├── sprite_manager.py      # Sprite loading and mood-based selection
├── .env                   # Stores Gemini API key (not included in repo)
├── log.txt                # Debug and error logs
└── README.md              # This file
```

---

## Usage

- **Chat**: Type your message and press Enter or click Send. The bot will reply with personality and display a matching sprite.
- **Weather**: Click "Check Weather" to get the current weather and see a themed sprite.
- **Rock Paper Scissors**: Click the button to play a quick game with the bot.
- **JoJo Mode**: Mention JoJo’s Bizarre Adventure characters or catchphrases for a surprise!
- **Exit**: Type `exit` or `quit` to close the app.

---

## Customization

- **Sprites**: Add PNG/GIF files to `assets/sprites/` with names starting with the mood (e.g., `happy1.png`, `sad2.gif`).
- **Sounds**: Replace or add WAV files in `assets/sfx/`.
- **Personality**: Edit `prompt_utils.py` to tweak trigger phrases or the bot’s style.
- **Minigames**: Expand `macncheese.py` to add more interactive features.

---

## Troubleshooting

- **No Response / Crashes**: Check `log.txt` for error details.
- **Sprites Not Showing**: Ensure all asset paths are correct and files exist.
- **Sound Issues**: Make sure `pygame` is installed and your system supports audio playback.
- **API Errors**: Double-check your `.env` file and API keys.

---

## Credits
- **Code & Design**: Harshit
- **Pixel Art**: Created in Pixel Studio app
- **APIs**: Google Gemini, OpenWeatherMap
- **Libraries**: Tkinter, Pillow, pygame, vaderSentiment, python-dotenv

---

## License
This project is for educational and personal use. All custom assets are original. Please do not redistribute without permission.

---