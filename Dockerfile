FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade poetry==2.1.1
COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY . /app

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
