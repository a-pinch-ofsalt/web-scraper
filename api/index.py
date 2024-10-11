from web_scraper import research_shallow
from flask import Flask, request, jsonify
import json
from urllib.parse import urljoin

app = Flask(__name__)

def handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    query = query_params.get('query', 'default query')

    # Your existing logic
    results = get_search_results(query)
    for item in results:
        crawl(item['link'])

    # Prepare the response
    response = {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(webpage_contents)
    }
    return response
