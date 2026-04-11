FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Fix line endings for run.sh (Windows CRLF -> Linux LF)
RUN sed -i 's/\r$//' run.sh && chmod +x run.sh

EXPOSE 7860

CMD ["./run.sh"]