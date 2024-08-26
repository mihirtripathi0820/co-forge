from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from prettytable import PrettyTable
app = Flask(__name__)
def create_database():
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            published_date TEXT,
            author TEXT,
            link TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()
create_database()
def get_distinct_authors():
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT author FROM articles")
    authors = [row[0] for row in cursor.fetchall()]
    conn.close()
    return authors
def get_distinct_titles():
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT title FROM articles")
    titles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return titles
def retrieve_articles(sort_by, search_publisher, search_title):
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()
    query = "SELECT * FROM articles WHERE 1"
    if search_publisher:
        query += f" AND author LIKE '%{search_publisher}%'"
    if search_title:
        query += f" AND title LIKE '%{search_title}%'"
    if sort_by == 'latest':
        query += " ORDER BY published_date DESC"
    elif sort_by == 'newest':
        query += " ORDER BY published_date ASC"
    elif sort_by == 'publisher':
        query += " ORDER BY author"
    query += " LIMIT 20"
    cursor.execute(query)
    articles = cursor.fetchall()
    conn.close()
    return articles
def retrieve_latest_articles():
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles ORDER BY published DESC LIMIT 20")
    articles = cursor.fetchall()
    conn.close()
    return articles
def retrieve_oldest_articles():
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles ORDER BY published ASC LIMIT 20")
    articles = cursor.fetchall()
    conn.close()
    return articles
@app.route('/')
def display_articles():
    sort_by = request.args.get('sort_by')
    search_publisher = request.args.get('search_publisher')
    search_title = request.args.get('search_title')
    if sort_by == 'latest':
        articles = retrieve_latest_articles()
    elif sort_by == 'oldest':
        articles = retrieve_oldest_articles()
    else:
        articles = retrieve_articles(sort_by, search_publisher, search_title)
    authors = get_distinct_authors()
    titles = get_distinct_titles()
    table = PrettyTable()
    table.field_names = ["ID", "Title", "Published", "Author", "Link", "Description"]
    for row in articles:
        table.add_row(row)
    return render_template('i.html', articles=table.get_html_string(), authors=authors, titles=titles)
@app.route('/latest_articles')
def display_latest_articles():
    articles = retrieve_latest_articles()
    authors = get_distinct_authors()
    table = PrettyTable()
    table.field_names = ["ID", "Title", "Published", "Author", "Link", "Description"]
    for row in articles:
        table.add_row(row)
    return render_template('i.html', articles=table.get_html_string(), authors=authors)
@app.route('/oldest_articles')
def display_oldest_articles():
    articles = retrieve_oldest_articles()
    authors = get_distinct_authors()
    table = PrettyTable()
    table.field_names = ["ID", "Title", "Published", "Author", "Link", "Description"]
    for row in articles:
        table.add_row(row)
    return render_template('i.html', articles=table.get_html_string(), authors=authors)
@app.route('/reset_filters')
def reset_filters():
    return redirect(url_for('display_articles'))
if __name__ == '__main__':
    app.run(debug=True)



