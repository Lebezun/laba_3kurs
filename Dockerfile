FROM python:3.11

WORKDIR /app

RUN pip install poetry

# ЗАБОРОНЯЄМО створювати віртуальне середовище всередині докера
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./
RUN poetry install --only main --no-root

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]