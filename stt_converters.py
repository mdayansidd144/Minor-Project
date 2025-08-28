# import speech_recognition as sr
# #this package is for the speech recognition and other packages are as follows
# recognizer = sr.Recognizer()
# with sr.Microphone() as source :
#     print("hello Say something...")
#     audio = recognizer.listen(source)
#     try:
#         print("you said:"+ recognizer.recognize_google(audio))
#     except sr.unknownValueError:
#         print("Sorry, i could not understand the audio.")
#     except sr.RequestError:
#         print("Could not connect to the service.")
# import pyttsx3
# engine = pyttsx3.init()
# engine.say("you said:"+recognizer.recognize_google(audio))
# engine.runAndWait()
# import tkinter as tk
# from tkinter import scrolledtext
# window= tk.Tk()
# window.geometry("400*200")
# text_area =  ScrolledText.ScrolledText(window,width=50,height = 10)
# text_area.pack()
import speech_recognition as sr
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

# Load pre-trained chatbot model and tokenizer and using the pip installer
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# function for the speech to text conversion
#each individual gets the three attempt
def speech_to_text(max_attempts=3):
    """Convert speech to text with retry mechanism."""
    for attempt in range(max_attempts):
        with sr.Microphone() as source:
            print("Listening...")
            engine.say("Please speak now.")
            engine.runAndWait()
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that.")
                engine.say("I didn't catch that. Please try again.")
                engine.runAndWait()
            except sr.RequestError:
                print("Sorry, there was an issue with the speech recognition service.")
                engine.say("There was an issue. Please try again.")
                engine.runAndWait()
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
                engine.say("No speech detected. Please try again.")
                engine.runAndWait()
    return None

#speech recognition for the ai voice to text conversion
def get_chatbot_response(user_input):
    """Generate chatbot response using the pre-trained model."""
    if not user_input:
        return "I didn't hear you or may be there is some noise. Could you please speak again?"

    # Encode input and generate response
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)

    # Simplify response for special education students commonly suffering from the dyslexia
    response = response.strip().lower()
    return response

#this is for the text interpreted by the speech using the modules
#this is about the text from the user
def text_to_speech(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def main():
    """Main function to run the chatbot."""
    print("Welcome to the AI Chatbot for Special Education!")
    engine.say("Welcome to the AI Chatbot! I'm here to help you.")
    engine.runAndWait()

    while True:
        # Get user input via speech
        user_input = speech_to_text()

        # Get and process chatbot response
        response = get_chatbot_response(user_input)
        print(f"Chatbot: {response}")
        text_to_speech(response)

        # Ask if the user wants to continue/or breaking the conversation
        text_to_speech("Would you like to ask another question?")
        continue_response = speech_to_text()
        if continue_response and "no" in continue_response.lower():
            print("Goodbye!")
            text_to_speech("Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        text_to_speech("Goodbye!")