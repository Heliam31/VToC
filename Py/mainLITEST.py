
from asyncio import run, set_event_loop_policy, WindowsSelectorEventLoopPolicy
from recordWin import speech_to_text
from os import remove, listdir, unlink, path, getcwd
from sys import exit
from time import time, sleep
from subprocess import Popen
from whisper import load_model
from threading import Thread
import string
import keyboard
import pyautogui
from pynput.mouse import Button, Controller, Listener
import Levenshtein


def on_click(x, y, button, pressed):
    if button == Button.x1:  # MB4 correspond généralement à Button.x1
        if pressed:
            user_message =  speech_to_text()
            print("message : ",user_message)
            start = time()
            phrase = user_message.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '')
            print("apres split : ",phrase)
            if user_message.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '') == "aurevoir":
                print("labite")
                exit(1)
            ouvre = ["ouvrezcetteporte","f5", "1"]
            croche = ["crochetezcette porte","f6", "1"]
            MLi = [ouvre,croche]
            smallerdist = [-1,-1]
            for i in range(len(MLi)):
                distance = Levenshtein.distance(phrase, MLi[i][0])
                print(f"Distance de Levenshtein : {distance}")
                if smallerdist == [-1,-1]:
                    smallerdist = [i,distance]
                if distance == 0:
                    smallerdist = [i,distance]
                    break
                if distance < smallerdist[1]:
                    smallerdist = [i, distance]
                
            if smallerdist != [-1,-1] and smallerdist[1] < 10:
                mouse = Controller()
                mouse.click(Button.middle)

                for zz in MLi[smallerdist[0]][1:]:
                    print("le ziziz ", zz)
                    pyautogui.press(zz)

            print(f"\n-------------------------Generated in {(time()-start)}s.-------------------------")
        else:
            print("Bouton MB4 relâché")

async def main():
    try:
        with Listener(on_click=on_click) as listener:    
            listener.join()
    except KeyboardInterrupt:
        exit(1)
    

if __name__ == "__main__":
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())    
    run(main())
    
    
