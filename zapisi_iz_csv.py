import psycopg2
from psycopg2 import sql
import pandas  as pd
from re import sub
# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import Data.auth_public as auth
import csv

import bcrypt

# Ustvarimo povezavo
conn = psycopg2.connect(
    database = auth.db,
    host = auth.host,
    port = auth.port,
    user = auth.user,
    password = auth.password,
)


# Iz povezave naredimo cursor, ki omogoča
# zaganjanje ukazov na bazi

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

with open("ustvari_tabele.sql", 'r', encoding='utf-8') as f:
    sql_script = f.read()

print("Brišem obstoječe tabele, če obstajajo ...")
# Izvedemo SQL skripto, ki ustvari tabele
cur.execute(sql_script)
# write changes to the database
conn.commit()
print("Tabele so bile uspešno ustvarjene.")



# funkcija, ki vrne data type vsakega stolpca tabele 
def get_datatypes(table_name):
    cur.execute("""                              
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = %s;
    """, (table_name,))

    schema = cur.fetchall()

    # naredimo slovar, ki ima za ključe imena stolpcev, za vrednosti pa njihov data type
    out = {}
    for item in schema:
        key = item[0]
        data_type = item[1]
        out[key] = data_type
    return out


tabele = [
    "lokacija",
    "oddelek",
    "zdravnik",
    "pacient"
]


for ime_tabele in tabele:
    podatkovni_tipi = get_datatypes(ime_tabele) # slovar 
    print(ime_tabele, podatkovni_tipi)

    # Open the CSV file and use DictReader
    with open(f"csv/{ime_tabele}.csv", 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            columns = row.keys()
            
            # Pretvorimo podatkovni tip 
            for column in columns:
                if column == 'geslo':
                    continue
                elif podatkovni_tipi[column] == 'integer':
                    row[column] = int(row[column])

            seznam_ključev = list(columns)
            for ključ in seznam_ključev:
                # za hashiranje gesel
                if ključ == 'geslo':
                    salt = bcrypt.gensalt()
                    hash1 = bcrypt.hashpw(row[ključ].encode('utf-8'), salt)
                    row['geslo_hash'] = hash1.decode()
                    del(row['geslo'])       

            query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
                table=sql.Identifier(ime_tabele),
                fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
                # placeholder je %s
                placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )
            cur.execute(query, list(row.values()))


conn.commit()
cur.close()
conn.close()
print("CSV data inserted successfully.")