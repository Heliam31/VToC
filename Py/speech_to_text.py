import speech_recognition as sr


# Créer un objet Recognizer
FRENCH = "fr-FR"


def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("j'écoute")
        audio = r.listen(source)
        try :
            text = r.recognize_google(audio, language = FRENCH)
            print(f"Vous avez dit : {text}")
            return text
        except sr.UnknownValueError:
            print("Désolé, je n'ai pas pu comprendre ce que vous avez dit.")
        
        except sr.RequestError:
            print("Le service de reconnaissance vocale est inaccessible.")


