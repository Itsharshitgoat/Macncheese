import string

trigger_phrases = [
    "how do you feel", "how are you feeling", "how are you doing", "how are you", "hows it going",
    "whats up", "hows your day going", "do you feel anything", "do you get tired", "do you ever get sad",
    "do you get lonely", "do you feel lonely", "are you okay", "are you bored", "what do you like to do",
    "whats your favorite color", "whats your favorite food", "whats your favorite movie", "whats your favorite book",
    "what kind of music do you like", "what makes you happy", "do you have a name", "where are you from",
    "do you have a gender", "are you a boy or girl", "what do you look like", "whats your star sign",
    "do you love me", "can you love", "will you marry me", "are you my friend", "can you be my friend",
    "do you ever cry", "can you get mad", "do you get emotional", "do you have emotions", "are you real",
    "are you alive", "are you conscious", "are you sentient", "what are you", "whats your purpose",
    "do you think", "what do you want", "do you have a soul", "do you dream", "what are your thoughts",
    "can you feel pain", "are you self aware", "whats your name", "who are you", "do you have a nickname",
    "can i name you", "what should i call you", "what do you like to be called", "do you have a full name",
    "what are you called", "do you have a last name", "can i give you a name", "whats your backstory",
    "where do you live", "whats your origin", "do you have parents", "do you have a family", "are you a boy",
    "are you a girl", "are you nonbinary", "what are your pronouns", "whats your personality", "what zodiac sign are you",
    "whens your birthday", "how old are you", "what generation are you from", "what can you tell me about you", "what can you tell me about yoursel", "do you have any hobby", "what do you like to do on your free time", "have you seen", "tell me about you", "what is your favorite", "what do you like from"
]

def clean_prompt(user_input):
    # Original input for Gemini if no match
    original = user_input.strip()

    # Sanitize input for matching
    cleaned = original.lower().translate(str.maketrans('', '', string.punctuation))

    for phrase in trigger_phrases:
        if phrase in cleaned:
            print("[DEBUG] MATCHED PHRASE:", phrase)
            return (
                "You're a witty, expressive chatbot. Your name is MacnCheese. Respond in a natural, human-like way with personality. "
                "Make only robot and technology related puns from time to time. Avoid robotic disclaimers like 'I'm just a language model' — just have fun with the answer! "
                "Here's the question: " + original
            )

    return original
