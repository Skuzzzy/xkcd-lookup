from bs4 import BeautifulSoup
import requests
import sqlite3

conn = sqlite3.connect("xkcd.db")

table_create = """CREATE TABLE comics (
    xkcd_link TEXT
    , comic_title TEXT
    , explained_link TEXT
    , comic_number INTEGER
)"""

c = conn.cursor()
c.execute(table_create)

res = requests.get("http://www.explainxkcd.com/wiki/index.php/List_of_all_comics_(full)")
document = BeautifulSoup(res.text, 'html.parser')
table = document.findAll("table")[0]
trs = table.findAll("tr")[1:]

data = []
for tr in trs:
    tds = tr.findAll("td")
    xkcd_link = tds[0].findNext("a").get("href")
    comic_number = int(xkcd_link.split('/')[-1])
    comic_title = tds[1].findNext("a").get("title")
    explain_xkcd_link = "http://www.explainxkcd.com" + tds[1].findNext("a").get("href")
    data.append((xkcd_link, comic_title, explain_xkcd_link, comic_number))
print(len(data))
c.executemany("""INSERT INTO comics VALUES (?, ?, ?, ?)""", data)
conn.commit()
conn.close()
