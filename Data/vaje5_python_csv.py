import psycopg2
import pandas  as pd
from re import sub
# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import auth_public as auth


database = auth.database
host = auth.host
port = auth.port
user = auth.user
password = auth.password

# Ustvarimo povezavo
conn = psycopg2.connect(database=database, host=host, port=port, user=user, password=password)


# Iz povezave naredimo cursor, ki omogoča
# zaganjanje ukazov na bazi

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)




def preberi_csv(ime_datoteke : str) -> pd.DataFrame:
    df = pd.read_csv(ime_datoteke, sep=",", index_col=0)

    return df



def zapisi_df(df: pd.DataFrame) -> None:

    ime_tabele = "zdravnik"

    # shranimo stolpce v seznam
    columns = df.columns.tolist()

    # Pretvorimo podatke v seznam tuple-ov
    records = df.values.tolist()
    
    # Pripravimo SQL ukaz za vstavljanje podatkov
    sql = f"INSERT INTO {ime_tabele} ({', '.join(columns)}) VALUES %s"
    
    # Uporabimo execute_values za množični vnos
    # Izvede po en insert ukaz na vrstico oziroma record iz seznama records
    # V odzadju zadeva deluje precej bolj optimlano kot en insert na ukaz!
    # Za množičen vnos je potrebno uporabiti psycopg2.extras.execute_values
    psycopg2.extras.execute_values(cur, sql, records)
    
    # Potrdimo spremembe v bazi
    conn.commit()


if __name__ == "__main__":
    # Preberi CSV datoteko, pri čemer privzamemo, da je datoteka
    # "customers-100.csv" v isti mapi kot tvoj skript ali podaj absolutno pot.
    df = preberi_csv("ZDRAVNIKI.csv")
    
    # Zapiši podatke iz DataFrame-a v tabelo "customers"
    zapisi_df(df)
    
    print("CSV datoteka je bila uspešno zabeležena v bazi.")