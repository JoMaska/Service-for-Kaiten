FROM python:3.11

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ .

RUN mkdir -p config && \
    cp config_example config/ && \
    cp secrets_example config/ && \
    cp spaces_example config/ && \
    cp env_example .

CMD ["uvicorn", "main:app", "--port", "8080"]
