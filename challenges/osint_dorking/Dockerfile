FROM python:3.11-alpine
WORKDIR /app
RUN pip install flask --quiet
COPY app.py .
EXPOSE 5006
CMD ["python", "app.py"]
