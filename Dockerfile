FROM --platform=linux/amd64 python:3.10
WORKDIR /app
COPY *.py config.ini *.txt /app/
COPY templates/index.html /app/templates/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 9000
CMD ["python", "healthprobe_flask.py"]