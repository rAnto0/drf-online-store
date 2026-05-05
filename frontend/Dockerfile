FROM python:3.11-slim
WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .

CMD ["uv", "run", "flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=5000"]
