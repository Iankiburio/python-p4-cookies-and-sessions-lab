from flask import Flask, jsonify, session, abort
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    # Initialize page_views in the session if it doesn't exist
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views for each request
    session['page_views'] += 1

    # Check if the user has viewed more than 3 pages
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Retrieve and return the article data
    # Replace this with your actual logic to fetch article data based on the id
    article = Article.query.get_or_404(id)
    article_data = {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date  # Include 'date' in the response
    }

    return jsonify(article_data)

if __name__ == '__main__':
    app.run(port=5555)
