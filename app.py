from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Lab Project - CI/CD Pipeline Running!</h1><p>Deployed via Jenkins on Kubernetes</p>'

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)