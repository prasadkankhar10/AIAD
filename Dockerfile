FROM python:3.9-slim

WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose port for Hugging Face Spaces (default is 7860)
EXPOSE 7860

# Run the FastAPI server using Uvicorn on port 7860
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
