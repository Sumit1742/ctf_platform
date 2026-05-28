FROM python:3.11-alpine
WORKDIR /app
RUN pip install flask --quiet
COPY app.py .
COPY files/ ./files/
EXPOSE 5016
CMD ["python", "app.py"]
