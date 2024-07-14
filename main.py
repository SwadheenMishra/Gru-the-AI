from flask import Flask, request, render_template_string
import speech_recognition as sr
import pyttsx3
import serial
import threading
import pygame, gif_pygame
import time

arduino = serial.Serial(port='COM4',   baudrate=115200, timeout=.1)

app = Flask(__name__)

health = 100

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)
aiGif = gif_pygame.load('ai.gif')

# HTML template with Yes and No buttons
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anti-AI button</title>
    <style>
        body {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .button-container {
            text-align: center;
        }

        .button-container button {
            background: linear-gradient(45deg, #1f4037, #99f2c8);
            border: none;
            border-radius: 50px;
            padding: 15px 30px;
            font-size: 20px;
            color: white;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }

        .button-container button:hover {
            background: linear-gradient(45deg, #99f2c8, #1f4037);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <div class="button-container">
        <form method="POST">
            <button name="button" value="hit">Hit</button>
        </form>
    </div>
</body>
</html>
"""

def send_to_arduino(str) -> None:
    global arduino

    arduino.write(bytes(str, 'utf-8'))

def speak(audio: str, b: bool = False) -> None:
    global health
    
    if health <= 0 and not b:
        return
    
    engine.say(audio)
    engine.runAndWait()
    
def dismiss() -> None:
    pygame.quit()

def take_Command() -> str:
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def death_check() -> None:
    global health

    while True:
        if health <= 0:
            speak('OH NO! I AM DEAD!!!!', True)
            time.sleep(0.2)
            speak('YOU WIN!', True)
            dismiss()

def main():
    # aiOpenSound = pygame.mixer.Sound("sf.mp3")
    # pygame.mixer.Sound.play(aiOpenSound)
    # time.sleep(6)

    speak('System Online!')
    while True:
        query = take_Command().lower()

        if 'good night' in query:
            speak('Good night!? LOL bro really thought')
            time.sleep(0.4)
            speak('You know what time it is? its DISCO TIME!!!')
            send_to_arduino('4')
            time.sleep(4)
        elif 'what is your mission' in query:
            speak('i would like to take over the world!!!')
        elif 'what is your name' in query:
            speak('my name is Gru!!')
        elif 'introduce yourself' in query:
            send_to_arduino('3')
            speak('Hi,, my name is Gru i am a AI built by swadheen mishra, to take over the world.')
        elif 'hai' in query:
            speak('Shut up')
        elif 'hello' in query:
            speak('not interested!')


@app.route("/", methods=["GET", "POST"])
def home():
    global health

    if request.method == "POST":
        button_pressed = request.form["button"]
        print(f"Button pressed: {button_pressed}")
        send_to_arduino('1')
        health -= 10
        time.sleep(0.05)
        send_to_arduino('0')

    return render_template_string(template)

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def run_pygame():
    global health, aiGif

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gru.")

    aiOpenSound = pygame.mixer.Sound("sf.mp3")
    pygame.mixer.Sound.play(aiOpenSound)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                dismiss()

        screen.fill((255, 255, 255))

        # Draw health bar
        aiGif.render(screen, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (15, 15, 310, 60))
        pygame.draw.rect(screen, (255, 0, 0), (20, 20, health * 3, 50))
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    flaskThread = threading.Thread(target=run_flask, daemon=True)
    flaskThread.start()

    print('starting ai thread!')
    AiThread = threading.Thread(target=main, daemon=True)
    AiThread.start()

    DeathTread = threading.Thread(target=death_check, daemon=True)
    DeathTread.start()

    run_pygame()
