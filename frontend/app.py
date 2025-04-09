from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/')
def index():
    api_url = 'http://127.0.0.1:8000/api/products/'
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        products = response.json()
        print(products)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        products = []

    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
