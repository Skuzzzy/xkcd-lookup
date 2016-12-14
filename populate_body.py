from bs4 import BeautifulSoup
import requests
import sqlite3

conn = sqlite3.connect("xkcd.db")

table_create = """CREATE TABLE explained (
    comic_text TEXT
    , explanation TEXT
    , comic_number INTEGER
)"""

c = conn.cursor()
# c.execute(table_create)

c = conn.cursor()
c.execute("""SELECT explained_link, comic_number FROM comics""")
explained_pages = c.fetchall()

explained_data = []
for link, comic_number in explained_pages:
    try:
        print(link, comic_number)
        res = requests.get(link)
        document = BeautifulSoup(res.text, "html.parser")
        iterator = document.find_all(id="Explanation")[0].find_parent().find_next_sibling()
        expl = []
        while iterator.name == 'p':
            expl.append(iterator.text)
            iterator = iterator.find_next_sibling()

        iterator = iterator.find_next_sibling('p')
        trans = []
        while iterator.name == 'p':
            trans.append(iterator.text)
            iterator = iterator.find_next_sibling()
        # explained_data.append((" ".join(expl), " ".join(trans), comic_number))
        explained_data.append((" ".join(trans), " ".join(expl), comic_number))
    except Exception as e:
        # I just don't care all that much
        print("Failed grabbing " + str(comic_number))

c.executemany("""INSERT INTO explained VALUES (?, ?, ?)""", explained_data)

conn.commit()
conn.close()
