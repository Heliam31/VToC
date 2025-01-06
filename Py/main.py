
from speech_to_text import speech_to_text
from os import remove, listdir, unlink, path, getcwd, _exit
from sys import exit
from time import time
import string
import pyautogui
from pynput.mouse import Button, Controller, Listener
import Levenshtein
import duckdb as dd



def on_click(x, y, button, pressed):
    if button == Button.x1:  # MB4 correspond généralement à Button.x1
        if pressed:
            user_message =  speech_to_text()
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
        else:
            print("Bouton MB4 relâché")

def main():
    try:
        with Listener(on_click=on_click) as listener:    
            listener.join()
    except KeyboardInterrupt:
        _exit(1)
    

if __name__ == "__main__": 
    main()
    
    
