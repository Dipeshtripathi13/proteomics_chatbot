
FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Install system dependencies for FAISS and other requirements
RUN apt-get update && apt-get install -y \
    libopenblas-dev \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

# Default command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
