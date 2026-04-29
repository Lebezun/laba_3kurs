
FROM python:3.11


WORKDIR /app


RUN pip install poetry


COPY . .


RUN poetry install --no-dev

CMD ["poetry", "run", "python", "run.py"]