
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

pressed = 0 

def on_click(x, y, button, pressed):
    if button == Button.x1:  # MB4 correspond généralement à Button.x1
        if pressed:
            user_message =  speech_to_text()
            print("message : ",user_message)
            start = time()
            phrase = user_message.lower().translate(str.maketrans("","", string.punctuation)).split()
            print("apres split : ",phrase)
            if user_message.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '') == "aurevoir":
                print("labite")
            cmdLi=[]
            if len(phrase) == 1: #Sur Hotage
                print("hotage")
                match phrase[0]:
                    case "menotte":
                        cmdLi.append("1")
                    case "viens":
                        cmdLi.append("2")
                        cmdLi.append("2")
                    case "stop":
                        cmdLi.append("2")
                        cmdLi.append("3")
            elif len(phrase) == 2: #Dans le vide manip equipe
                match phrase[0]:
                    case "jaune":
                        cmdLi.append("f5")
                    case "bleu":
                        cmdLi.append("f6")
                    case "rouge":
                        cmdLi.append("f7")
                    case _:                                                                                               
                        print("Commande inconnue")
            
                match phrase[1]:
                    case "ici":
                        cmdLi.append("1")
                    case "finalisation":
                        cmdLi.append("6")
                    case "un":
                        cmdLi.append("2")
                        cmdLi.append("1")
                    case "deux":
                        cmdLi.append("2")
                        cmdLi.append("2")   
                    case "diamant":
                        cmdLi.append("2")
                        cmdLi.append("3")   
                    case "triangle":
                        cmdLi.append("2")
                        cmdLi.append("4")              
            elif len(phrase) == 3:
                match phrase[0]:
                    case "jaune":
                        cmdLi.append("f5")
                    case "bleu":
                        cmdLi.append("f6")
                    case "rouge":
                        cmdLi.append("f7")
                    case _:                                                                                               
                        print("Commande inconnue")
                
                match phrase[1]:
                    case "rassemblement":
                        cmdLi.append("1")
                        match phrase[2]:
                            case "séparer":
                                cmdLi.append("1")
                            case "gauche":
                                cmdLi.append("2")
                            case "droite":
                                cmdLi.append("3")
                    case "entrer":
                        cmdLi.append("2")

                        match phrase[2]:
                            case "propre":
                                cmdLi.append("1")
                            case "aveuglante":
                                cmdLi.append("2")
                            case "lacrymogène":
                                cmdLi.append("3")

                    case "destruction":
                        cmdLi.append("3")

                        match phrase[2]:
                            case "pied":
                                cmdLi.append("1")
                                cmdLi.append("1")
                            case "pompe":
                                cmdLi.append("2")
                                cmdLi.append("1")
                            case "bombe":
                                cmdLi.append("3")
                                cmdLi.append("1")
                    

            mouse = Controller()
            mouse.click(Button.middle)
            print(cmdLi)
            for zz in cmdLi:
                pyautogui.press(zz)

            print(f"\n-------------------------Generated in {(time()-start)}s.-------------------------")
        else:
            print("Bouton MB4 relâché")

async def main():
    with Listener(on_click=on_click) as listener:    
        listener.join()
                
    

if __name__ == "__main__":
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())    
    run(main())
    
    
