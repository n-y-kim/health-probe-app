FROM --platform=linux/amd64 python:3.10
WORKDIR /app
COPY *.py *.txt config.ini /app/
RUN apt-get update && apt-get install -y cron
RUN pip install --no-cache-dir -r requirements.txt
RUN (crontab -l ; echo "* * * * * cd /app && /usr/local/bin/python3 /app/delete_vmss_instance.py >> /app/log/delete_vmss_instance.log 2>&1") | crontab
CMD ["cron", "-f"]

# save image as delete-app