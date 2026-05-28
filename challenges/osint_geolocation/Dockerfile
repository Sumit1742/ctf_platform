FROM python:3.11-alpine
WORKDIR /app
RUN pip install flask --quiet
COPY app.py .
COPY suspicious.jpg .
EXPOSE 5007
CMD ["python", "app.py"]
