FROM --platform=linux/amd64 python:3.10
WORKDIR /app
COPY *.py *.txt config.ini /app/
RUN apt-get update && apt-get install -y cron
RUN pip install --no-cache-dir -r requirements.txt
RUN (crontab -l ; echo "* * * * * cd /app && /usr/local/bin/python3 /app/metric_collector.py >> /app/log/metric_cron.log 2>&1") | crontab
CMD ["cron", "-f"]

# Save image as metric-app