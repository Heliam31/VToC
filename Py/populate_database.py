import duckdb as dd

# Create a persistent DuckDB database
con = dd.connect('my_database.db')

try:
    result = con.execute('SELECT * FROM phrases').fetchall()
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

res = con.execute('SELECT phrase FROM phrases').fetchall()
# print(res[0][0])

finaj = ""
for i in res:
    print("lignaj : ",i[0])
    if i[0] == 'ouvrezcetteporte':
        finaj = i[0]

res = con.execute("SELECT commands FROM phrases WHERE phrase = \'" + finaj + "\';").fetchall()
print(res[0][0])