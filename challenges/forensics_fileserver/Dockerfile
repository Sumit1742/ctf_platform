FROM python:3.11-slim
WORKDIR /app
RUN pip install flask --no-cache-dir
COPY app.py .
COPY challenge_files/ ./challenge_files/
EXPOSE 5011
CMD ["python", "app.py"]
