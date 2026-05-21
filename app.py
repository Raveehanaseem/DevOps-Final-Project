from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('webapp_requests_total', 'Total requests')

@app.route('/')
def home():
    REQUEST_COUNT.inc()
    return '<h1>Lab Project - CI/CD Pipeline Running!</h1><p>Deployed via Jenkins on Kubernetes</p>'

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)