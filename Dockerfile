FROM python:3.9-slim

WORKDIR /app

# This version ignores SSL/DNS certificate errors that often happen in WSL
RUN pip install --no-cache-dir --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org flask

COPY app.py .

CMD ["python", "app.py"]
