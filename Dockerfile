FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860
EXPOSE 8501

RUN chmod +x run.sh

CMD ["./run.sh"]