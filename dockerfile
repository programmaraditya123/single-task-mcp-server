FROM python:3.11-slim

WORKDIR /app
COPY . .

# Install uv first, then export and install dependencies
RUN pip install --no-cache-dir uv \
 && uv export --format requirements.txt > requirements.txt \
 && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
