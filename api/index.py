from web_scraper import research_shallow
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scrape_web', methods=['POST'])
def index():
    data = request.get_json()
    query = data.get('query')
    return jsonify({'message': research_shallow(query)})