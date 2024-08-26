from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from prettytable import PrettyTable

app = Flask(__name__)

# Function to create the database and table
def create_database():
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()

    # Create the articles table with the necessary columns
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

# Create the database and table if they don't exist
create_database()

# Function to retrieve distinct authors
def get_distinct_authors():
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()

    # Query to retrieve distinct authors
    cursor.execute("SELECT DISTINCT author FROM articles")
    authors = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return authors

# Function to retrieve distinct titles
def get_distinct_titles():
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()

    # Query to retrieve distinct titles
    cursor.execute("SELECT DISTINCT title FROM articles")
    titles = [row[0] for row in cursor.fetchall()]

    conn.close()
    return titles

# Function to retrieve articles based on sorting and search criteria
def retrieve_articles(sort_by, search_publisher, search_title):
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()

    # Base query to retrieve articles
    query = "SELECT * FROM articles WHERE 1"

    # Check if a search query for the publisher is provided
    if search_publisher:
        query += f" AND author LIKE '%{search_publisher}%'"

    # Check if a search query for the title is provided
    if search_title:
        query += f" AND title LIKE '%{search_title}%'"

    # Add sorting criteria
    if sort_by == 'latest':
        query += " ORDER BY published_date DESC"
    elif sort_by == 'newest':
        query += " ORDER BY published_date ASC"
    elif sort_by == 'publisher':
        query += " ORDER BY author"

    # Limit the results to 20
    query += " LIMIT 20"

    cursor.execute(query)
    articles = cursor.fetchall()
    conn.close()
    return articles

# Function to retrieve the latest news articles
def retrieve_latest_articles():
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles ORDER BY published DESC LIMIT 20")
    articles = cursor.fetchall()
    conn.close()
    return articles

# Function to retrieve the oldest news articles
def retrieve_oldest_articles():
    conn = sqlite3.connect('news_articles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles ORDER BY published ASC LIMIT 20")
    articles = cursor.fetchall()
    conn.close()
    return articles

# Create a route to display articles
@app.route('/')
def display_articles():
    # Get the filtering parameters from the URL
    sort_by = request.args.get('sort_by')
    search_publisher = request.args.get('search_publisher')
    search_title = request.args.get('search_title')

    # Handle the sorting criteria
    if sort_by == 'latest':
        articles = retrieve_latest_articles()
    elif sort_by == 'oldest':
        articles = retrieve_oldest_articles()
    else:
        articles = retrieve_articles(sort_by, search_publisher, search_title)

    # Retrieve distinct authors for the author search bar
    authors = get_distinct_authors()

    # Retrieve distinct titles for the title filter
    titles = get_distinct_titles()

    # Create a PrettyTable to format the articles
    table = PrettyTable()
    table.field_names = ["ID", "Title", "Published", "Author", "Link", "Description"]
    for row in articles:
        table.add_row(row)

    return render_template('i.html', articles=table.get_html_string(), authors=authors, titles=titles)

# Route to display the latest news articles
@app.route('/latest_articles')
def display_latest_articles():
    articles = retrieve_latest_articles()
    authors = get_distinct_authors()
    table = PrettyTable()
    table.field_names = ["ID", "Title", "Published", "Author", "Link", "Description"]
    for row in articles:
        table.add_row(row)
    return render_template('i.html', articles=table.get_html_string(), authors=authors)

# Route to display the oldest news articles
@app.route('/oldest_articles')
def display_oldest_articles():
    articles = retrieve_oldest_articles()
    authors = get_distinct_authors()
    table = PrettyTable()
    table.field_names = ["ID", "Title", "Published", "Author", "Link", "Description"]
    for row in articles:
        table.add_row(row)
    return render_template('i.html', articles=table.get_html_string(), authors=authors)

# Route to reset all filters and return to the default view
@app.route('/reset_filters')
def reset_filters():
    # Redirect to the default route without any filters
    return redirect(url_for('display_articles'))

if __name__ == '__main__':
    app.run(debug=True)



