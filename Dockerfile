FROM python:3.10-slim
WORKDIR /app
COPY *.py config.ini /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 9000
CMD ["./healthprobe_flask.py"]