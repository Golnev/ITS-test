FROM python:3.13.0

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["sh", "./run_tests.sh"]