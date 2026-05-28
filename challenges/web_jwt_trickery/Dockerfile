FROM python:3.11-alpine
WORKDIR /app
RUN pip install flask PyJWT --quiet
COPY app.py .
EXPOSE 5005
CMD ["python", "app.py"]
