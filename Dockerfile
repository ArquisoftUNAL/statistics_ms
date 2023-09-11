FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY . /code
RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]