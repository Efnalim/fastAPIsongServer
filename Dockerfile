FROM python:3.9-slim

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["uvicorn", "router.main:app", "--host", "0.0.0.0", "--port", "8000"]