* * * * * cd ~/scripts/health-probe-app && ./metric_collector.py >> ~/metric_cron.log 2>&1
* * * * * cd ~/scripts/health-probe-app && ./delete_vmss_instance.py >> ~/delete_vmss_instance.log 2>&1
