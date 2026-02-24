# 1. Use a rock-solid, stable Python version
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements and install them securely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your actual API code into the container
COPY main.py .

# 5. Run the API using gunicorn (Production-grade server)
# Note: We use main:app because your file is named main.py!
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app