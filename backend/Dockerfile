FROM python:3.9-slim

# Force python to send logs straight to terminal
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Re-run install with a clean slate
RUN pip install --no-cache-dir flask flask-cors

COPY app.py .

CMD ["python", "app.py"]
