import duckdb as dd
import string
from os import _exit

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
        con.execute('''
        INSERT INTO phrases VALUES
        ('ouvrezcetteporte', ARRAY['f5', '1']),
        ('crochetezcetteporte', ARRAY['f6', '1']);
        ''')

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
                # keysg = f"'{key}'"
                keyLi.append(key)
                print("liste des commandes ", keyLi)
            
        print("ajout de votre commande à notre base de données")
        con.execute(f'''
        INSERT INTO phrases VALUES
        ('{user_message.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '')}', ARRAY{keyLi});
        ''')

        result = con.execute(f"SELECT * FROM phrases WHERE phrase = '{user_message.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '')}';").fetchall()
        print("commande ajoutée : \n", result)
        key = input("Voulez vous entrer une autre commande? yes or no : ")
        if key.lower().translate(str.maketrans("","", string.punctuation)).replace(' ', '') != "yes":
            done = 1

if __name__ == "__main__": 
    populate_database()