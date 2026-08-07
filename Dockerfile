FROM python:3.11-slim

# Why 3.11?
# Tumhara project Python 3.11 pe test hua hai.
# Cloud me bhi wahi version use karenge.

# Why slim?
# Comparison
# Image	Approx Size
# python:3.11	~1 GB
# python:3.11-slim	~150 MB
# python:3.11-alpine	~60 MB

ENV PYTHONUNBUFFERED=1
# CloudWatch me logs immediately dikhenge.
ENV PYTHONDONTWRITEBYTECODE=1
# Container me .pyc files nahi banengi.Image clean rahegi.

# Set the application working directory.
WORKDIR /app
#Container ke andar app naam ka folder ban jayega.
#sab app ke ander hi execute hoga

# Install dependencies first to improve Docker layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --no-cache-dir Matlab
# pip apna cache, image me store nahi karega.
# Image should be smaller, it will store somewhere else



# Copy the application source after dependencies are installed.
COPY . .
# ab pura project copy hoga.Isliye Ye
# Last me hona chahiye.

# Streamlit serves the application on port 8501.
EXPOSE 8501
# Yaha ek misconception hai.Ye Port open
# Nahi karta.Sirf Documentation hai.
# Docker ko batata hai Application 8501
# pe chalegi.
# Real port mapping Hota hai
# docker run -p 8501:8501


# Run Streamlit in headless mode for containerized environments.
CMD ["streamlit","run","app.py","--server.address=0.0.0.0","--server.headless=true"]

# CMD vs ENTRYPOINT
# CMD, Default command, Replace ho sakti hai.

# ENTRYPOINT, Fixed command, Replace nahi hoti.
# Hum Streamlit use kar rahe hain.
# CMD perfect.


#Docker layers
# Layer 1
# Python

# Layer 2
# requirements.txt

# Layer 3
# pip install

# Layer 4
# Copy source