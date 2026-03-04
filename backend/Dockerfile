FROM python:3.10-slim

WORKDIR /code

# Install system dependencies required for OpenCV / Unstructured
RUN apt-get update && apt-get install -y \
    gcc \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./app /code/app

# Create storage directories
RUN mkdir -p /code/storage/uploads
RUN mkdir -p /code/storage/processed

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]