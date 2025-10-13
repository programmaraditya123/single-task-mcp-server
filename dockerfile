FROM python:3.10-slim

# 🧩 Install system dependencies
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libxrender1 libxext6 libsm6 libice6 libcrypt1

# 🧠 Upgrade pip and install requirements
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# 🚀 Copy and run your app
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
