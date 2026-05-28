FROM python:3.11-slim
WORKDIR /app
RUN pip install flask --no-cache-dir
COPY app.py .
ENV FLAG="CTF{sql_1nj3ct10n_f0r_th3_w1n}"
EXPOSE 5000
CMD ["python", "app.py"]
