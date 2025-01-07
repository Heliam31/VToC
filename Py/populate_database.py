import duckdb as dd
import string
from os import _exit
import json

from speech_to_text import speech_to_text

def populate_database():
    # Create a persistent DuckDB database
    con = dd.connect('my_database.db')

    try:
        result = con.execute('SELECT phrase FROM phrases').fetchall()
        print("Données existantes :", result)
    except dd.CatalogException:
        print("Aucune table trouvée, vous pouvez en créer de nouvelles.")
        con.execute('''
        CREATE TABLE phrases (
            phrase TEXT,
            commands TEXT[]
        );
        ''')
        print("Table 'phrases' créée.")

        # Insert some data
        # con.execute('''
        # INSERT INTO phrases VALUES
        # ('ouvrezcetteporte', ARRAY['f5', '1']),
        # ('crochetezcetteporte', ARRAY['f6', '1']);
        # ''')

    print("Bienvenue, dites la phrase que vous voulez ajouter")
    done = 0
    while not done:
        user_message = ""
        good = 0
        while not good:
            user_message =  speech_to_text()
            ans = input("Est-ce le bon message? yes to confirm, no to retry stop to close the program : ")
            if ans.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '') == "yes":
                good = 1
            if ans.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '') == "stop":
                print("Closing the program")
                _exit(1)

        print("Bien vous pouvez maintenant entre les macros associées a cette commande, une touche par une, envoyez stop une fois terminé")
        keyLi = []
        good = 0
        while not good:
            key = input("Entrez une touche : ")
            if key.lower().replace(' ', '') == "stop":
                good = 1
            else:
                keyLi.append(key)
                print("liste des commandes ", keyLi)
            
        print("ajout de votre commande à notre base de données")

        #Add to json for save
        try:
            with open("phrases.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        new_data = {
            "phrase": user_message,
            "commands": keyLi
        }

        data.append(new_data)

        with open("phrases.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        #Add to db
        con.execute(f'''
        INSERT INTO phrases VALUES
        ('{user_message.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '')}', ARRAY{keyLi});
        ''')

        result = con.execute(f"SELECT * FROM phrases WHERE phrase = '{user_message.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '')}';").fetchall()
        print("commande ajoutée : \n", result)
        key = input("Voulez vous entrer une autre commande? yes or no : ")
        if key.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '') != "yes":
            done = 1

def modif_database():
    con = dd.connect('my_database.db')

    try:
        result = con.execute('SELECT * FROM phrases').fetchall()
        print("Données existantes :", result)
    except dd.CatalogException:
        print("Aucune table trouvée, vous pouvez en créer de nouvelles.")

    print("Dites moi la phrase que vous voulez modifier : ")
    done = 0
    while not done:
        good = 0
        while not good:
            phrase_to_modif =  speech_to_text()
            ans = input("c'est bien cette phrase? yes or no \n")
            if ans == "yes":
                good = 1
            else:
                print("Répétez la phrase")

        ans = input("Que voulez vous faire? modif_phrase / modif_command / supprimer : ")
        match ans:
            case "modif_phrase":
                phrase = ""
                print("donnez la phrase que vous voulez dire a la place de : ", phrase_to_modif)
                good = 0
                while not good:
                    phrase =  speech_to_text()
                    ans = input("c'est bien cette phrase? yes or no \n")
                    if ans == "yes":
                        good = 1
                    else:
                        print("Répétez la phrase")

                con.execute(f'''
                    UPDATE phrases
                    SET phrase = '{phrase.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '')}'

                    WHERE phrase = {phrase_to_modif.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '')};
                ''')

                print("la phrase a bien été modifiée")
            case "modif_command":
                cmd_list = []

                print("Donnez nous la nouvelle combinaison, une touche par une, envoyez stop une fois terminé")
                good = 0
                while not good:
                    key = input("Entrez une touche : ")
                    if key.lower().replace(' ', '') == "stop":
                        good = 1
                    else:
                        cmd_list.append(key)
                        print("liste des commandes ", cmd_list)

                con.execute(f'''
                    UPDATE phrases
                    SET commands = ARRAY{cmd_list}
                    WHERE phrase = '{phrase_to_modif.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '')}';
                ''')

                print("commande modifiée!")

            case "supprimer":
                print("suppression de la phrase : ", phrase_to_modif)
                con.execute(f'''
                    DELETE FROM phrases
                    WHERE phrase = '{phrase_to_modif.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '')}';
                ''')

                print("suppression terminée")

        result = con.execute('SELECT * FROM phrases').fetchall()
        print("Nouvelle DB :", result)
        ans = input("Voulez vous faire une autre action? yes or no : ")
        if ans == "yes":
            print("d'accord dites moi la phrase a modifier")
        elif ans == "no":
            done = 1
        else:
            print("bah nique ta mère")


if __name__ == "__main__": 
    ans = input("Bonjour, voulez vous ajouter des élements ou en modifier/supprimer? ajouter ou modifier :\n")
    if ans == "ajouter":
        populate_database()
    elif ans == "modifier":
        modif_database()
    else:
        print("bah nique ta mère")