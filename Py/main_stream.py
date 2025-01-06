
import speech_recognition as sr
from os import _exit
from time import time
import string
import pyautogui
from pynput.mouse import Button, Controller
import Levenshtein
import duckdb as dd

recognizer = sr.Recognizer()

def traiter(user_message):
    start = time()
    phrase = user_message.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '')

    if user_message.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '') == "aurevoir":
        print("Exit message detecté, bye")
        _exit(1)

    #Base de phrases
    commands = ""
    con = dd.connect('my_database.db')

    try:
        result = con.execute(f"SELECT commands FROM phrases WHERE phrase = '{phrase}';").fetchall()
    except dd.CatalogException:
        print("[ERROR] Base de données vide, créez votre base de phrases")

    if result:
        commands = result
        print("Trouvé correspondance")
    else: 
        # On a pas trouvé exactement la phrase  
        ph_list = con.execute('SELECT phrase FROM phrases').fetchall()

        #Comparaison de notre phrase à celles de la base
        smallerdist = ["",-1]
        for ph in ph_list:
            distance = Levenshtein.distance(phrase, ph[0])
            # print(f"Distance de Levenshtein : {distance}")
            if smallerdist == ["",-1]:
                smallerdist = [ph[0],distance]
            if distance == 0:
                smallerdist = [ph[0],distance]
                break
            if distance < smallerdist[1]:
                smallerdist = [ph[0], distance]
            
        print(f"phrase sélectionnée : {smallerdist[0]} avec confiance {smallerdist[1]}")
        if smallerdist != ["",-1] and smallerdist[1] < 5:
            commands = con.execute("SELECT commands FROM phrases WHERE phrase = \'" + smallerdist[0] + "\';").fetchall()
    # Si on a selectionné une phrase de la base et que sa distance est < 10 mots
    if commands != "":
        mouse = Controller()
        mouse.click(Button.middle)

        for zz in commands[0][0]:
            print("pressing :  ", zz)
            pyautogui.press(zz)
    else:
        print("pas de commande trouvée")

    print(f"\n-------------------------Generated in {(time()-start)}s.-------------------------")


def listen_continuously():
    with sr.Microphone() as source:
        print("Calibration du microphone, veuillez attendre...")
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Ajuste au bruit ambiant
        print("Prêt, parlez !")

        while True:
            try:
                # Écoute l'audio
                print("Écoute...")
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)

                # Reconnaissance vocale
                print("Reconnaissance en cours...")
                text = recognizer.recognize_google(audio, language="fr-FR")  # Langue en français
                print(f"Vous avez dit : {text}")

                traiter(text)

            except sr.UnknownValueError:
                print("Je n'ai pas compris, pouvez-vous répéter ?")
            except sr.RequestError as e:
                print(f"Erreur du service de reconnaissance vocale : {e}")
            except KeyboardInterrupt:
                print("Programme interrompu.")
                break





def main():
    try:
        listen_continuously()
    except KeyboardInterrupt:
        _exit(1)
    

if __name__ == "__main__": 
    main()
    
    
