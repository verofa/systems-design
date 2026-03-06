from flask import Flask, request, redirect, url_for, jsonify
import random
import string
import sqlite3
from urllib.parse import urlparse

app = Flask(__name__)

# Generate short code - 6 alphanumeric characters
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL'}), 400
    
    long_url = data['url']
    parsed = urlparse(long_url)
    if not parsed.scheme or not parsed.netloc:
        return jsonify({'error': 'Invalid URL'}), 400
    
    # Check if the URL exist in database and get i
    conn = sqlite3.connect('tinyurl.db')
    cursor = conn.cursor()
    cursor.execute('SELECT short_code FROM urls WHERE long_url = ?', (long_url,))
    result = cursor.fetchone()
    conn.close()

    if result:
        short_url = f'http://localhost:5000/{result[0]}'
        return jsonify({'short_url': short_url}), 200
    
    # If does not exist, generate new shot code and store
    short_code = generate_short_code()
    conn = sqlite3.connect('tinyurl.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO urls (long_url, short_code) VALUES (?, ?)',
        (long_url, short_code))
    conn.commit()
    conn.close()
    
    short_url = f'http://localhost:5000/{short_code}'
    return jsonify({'short_url': short_url}), 201

@app.route('/<short_code>')
def redirect_url(short_code):
    conn = sqlite3.connect('tinyurl.db')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_code = ?', (short_code,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
