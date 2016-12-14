from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from scipy import spatial
from sklearn.metrics.pairwise import euclidean_distances
import sqlite3

conn = sqlite3.connect("xkcd.db")

c = conn.cursor()
c.execute("""SELECT comic_text, explanation, comic_number FROM explained""")
explained_pages = c.fetchall()

explained_data = []
labels = []
for comic_text, explanation, comic_number in explained_pages:
    explained_data.append("\n".join([comic_text, explanation]).lower())
    labels.append(comic_number)

vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
vectors = vectorizer.fit_transform(explained_data)
# print(vectorizer.vocabulary_)


while True:
    test = raw_input("Enter Search Query> ").lower()
    vector = vectorizer.transform([test])
    distances = (euclidean_distances(vectors, vector))
    results = (sorted(zip(distances, labels), key=lambda v:v[0]))
    query = """SELECT xkcd_link, comic_title FROM comics WHERE comic_number=?"""
    for result in results[:5]:
        c.execute(query, (result[1],))
        print(c.fetchone())

conn.close()
