from flask import Flask, render_template, request, session, redirect, url_for, flash
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Замените на безопасный секретный ключ
API_BASE_URL = "http://main-api:8000/api"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "access_token" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    # Получение параметров фильтрации
    category = request.args.get("category")
    search = request.args.get("search")
    ordering = request.args.get("ordering")

    # Формирование параметров запроса
    params = {}
    if category:
        params["category__slug"] = category
    if search:
        params["search"] = search
    if ordering:
        params["ordering"] = ordering

    # Инициализация переменных с безопасными значениями по умолчанию
    products = {"results": []}
    categories = []
    cart = {"items": []}  # Устанавливаем безопасное значение по умолчанию
    try:
        # Получение списка продуктов с фильтрацией
        response = requests.get(f"{API_BASE_URL}/products/", params=params)
        response.raise_for_status()
        products = response.json()
        # Получение категорий для фильтра
        categories_response = requests.get(f"{API_BASE_URL}/categories/")
        categories_response.raise_for_status()
        categories = categories_response.json()
        # Получение корзины, если пользователь авторизован
        if "access_token" in session:
            headers = {"Authorization": f'Bearer {session["access_token"]}'}
            try:
                cart_response = requests.get(f"{API_BASE_URL}/cart/", headers=headers)
                if cart_response.status_code == 200:
                    cart_data = cart_response.json()
                    # Проверяем структуру полученных данных
                    if isinstance(cart_data, dict) and "items" in cart_data:
                        cart = cart_data
                    else:
                        print("Некорректная структура данных корзины")
                        cart = {"items": []}
                else:
                    print(f"Ошибка получения корзины: {cart_response.status_code}")
                    cart = {"items": []}
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе корзины: {e}")
                cart = {"items": []}

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}")

    return render_template(
        "index.html",
        products=products,
        categories=categories,
        cart=cart,  # Теперь cart всегда будет иметь структуру {"items": [...]}
        current_category=category,
        current_search=search,
        current_ordering=ordering,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = {
            "username": request.form["username"],
            "password": request.form["password"],
        }
        try:
            response = requests.post(f"{API_BASE_URL}/accounts/token/", json=data)
            if response.status_code == 200:
                tokens = response.json()
                session["access_token"] = tokens["access"]
                session["refresh_token"] = tokens["refresh"]
                return redirect(url_for("index"))
            else:
                flash("Неверные учетные данные")
        except requests.exceptions.RequestException:
            flash("Ошибка сервера")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "username": request.form["username"],
            "email": request.form["email"],
            "password": request.form["password"],
        }
        try:
            # Отправляем запрос на регистрацию
            response = requests.post(f"{API_BASE_URL}/accounts/register/", json=data)
            if response.status_code == 201:
                # После успешной регистрации, выполняем вход
                login_response = requests.post(
                    f"{API_BASE_URL}/accounts/token/",
                    json={"username": data["username"], "password": data["password"]},
                )
                if login_response.status_code == 200:
                    tokens = login_response.json()
                    session["access_token"] = tokens["access"]
                    session["refresh_token"] = tokens["refresh"]
                    return redirect(url_for("index"))
                else:
                    flash("Регистрация успешна, но возникла ошибка при входе")
            else:
                error_message = response.json()
                flash(str(error_message))
        except requests.exceptions.RequestException:
            flash("Ошибка сервера при регистрации")
    return render_template("register.html")


@app.route("/cart")
@login_required
def cart():
    try:
        headers = {"Authorization": f'Bearer {session["access_token"]}'}
        response = requests.get(f"{API_BASE_URL}/cart/", headers=headers)
        cart_data = {"items": []}  # Значение по умолчанию
        
        if response.status_code == 200:
            try:
                cart_data = response.json()
                if not isinstance(cart_data, dict):
                    cart_data = {"items": []}
                elif "items" not in cart_data:
                    cart_data["items"] = []
            except (ValueError, TypeError):
                # Если возникла ошибка при разборе JSON
                cart_data = {"items": []}
                
    except requests.exceptions.RequestException:
        cart_data = {"items": []}
        
    return render_template("cart.html", cart=cart_data)


@app.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    try:
        headers = {"Authorization": f'Bearer {session["access_token"]}'}
        data = {
            "product_id": product_id,
            "quantity": int(request.form.get("quantity", 1)),
        }
        response = requests.post(
            f"{API_BASE_URL}/cart/items/", headers=headers, json=data
        )
        if response.status_code == 201:
            flash("Товар добавлен в корзину")
        else:
            flash("Ошибка при добавлении товара")
    except requests.exceptions.RequestException:
        flash("Ошибка сервера")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    # Очищаем данные сессии
    session.pop("access_token", None)
    session.pop("refresh_token", None)
    flash("Вы успешно вышли из системы")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
