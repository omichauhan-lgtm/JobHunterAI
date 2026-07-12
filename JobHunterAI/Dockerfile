# Use official python slim image
FROM python:3.12-slim

# Install system dependencies (including pdflatex for LaTeX compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source files
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Default CMD runs the FastAPI API Gateway
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]
