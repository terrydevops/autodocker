# Project Setup Guide

## Architecture design

Considering the requirement to avoid using Kubernetes and only use docker-compose, we can utilize Prometheus' monitoring capabilities combined with webhooks. This approach will call server-side APIs to trigger docker-compose scale. This forms the core principle of this version.

![WX20240805-202220@2x](https://github.com/user-attachments/assets/cef7a104-a489-43a9-ae75-7b51832430f6)


## Install Docker Compose

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/v2.2.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Change Alertmanager Webhook Address

Open the config/alertmanager.yml file and update the webhook address. For example:

```sh
receivers:
  - name: 'webhook'
    webhook_configs:
      - url: 'http://new-webhook-address'
```


## Enable the Controller
This controller is a key compoent running as webhook for alertmangerxss 
```sh
sudo apt update
sudo apt install -y python3 python3-pip
sudo apt install python3.12-venv 
python3 -m venv myenv
source myenv/bin/activate
pip3 install Flask python_on_whales
nohup python3 controller.py  &
```

## Start the Web App
```sh
sudo apt install docker.io
sudo systemctl start docker
cd autodocker/
sudo docker-compose up -d
```

## Test
Enable Jmeter GUI, test with url: http://xx.xx.xx.xx:8088/system_info
You will see the docker scall up and down accrdingly. 
![image-docker-compose](https://github.com/user-attachments/assets/f53e5f38-6e9c-45ab-82d0-4a37ac10111e)


# TODO:

## Network Isolation:
Problem: Network isolation prevents access to monitoring metrics.
Solution: Use service discovery or DNS-based service names to avoid hardcoding IP addresses. Implement a proxy layer to facilitate data transfer.

## Hardcoded cAdvisor IP:
Problem: The IP address for cAdvisor is hardcoded, leading to potential issues.
Solution: Use dynamic service discovery or container networking features in Docker to avoid hardcoding IPs.

## Monitoring Metrics:
Problem: Deciding whether to use single container metrics, average, or maximum values.
Solution: Temporarily use average (avg). For more robust monitoring, consider combining different metrics and thoroughly testing different scenarios.


## Difficulty Hitting Target Range:
Problem: Adjusting many values to hit the target range without overloading.
Solution: Use a more dynamic approach to setting thresholds and incorporate feedback loops to adjust thresholds based on real-time data.

## Memory Allocation and Alerts:
Problem: Default memory allocation (50M) exceeds the alert threshold.
Solution: Adjust the default memory allocation and alert thresholds to better match the actual usage patterns.

## Alert Sensitivity:
Problem: Alert trigger time (1 minute) is too insensitive.
Solution: Temporarily change the alert trigger time to 15 seconds and consider the metric scraping interval for consistency.

## Consistency of firing and resolved Times:
Problem: Ensuring consistency between firing and resolved times.
Solution: Synchronize the timing of alerts and ensure they reflect the actual state changes accurately.

## One-Time Alert Exceedance:
Problem: Alert exceeding only once leads to a single scaling action, with no further scaling if still insufficient.
Solution: Implement a more continuous monitoring and alerting system that can trigger multiple scaling actions if needed.

## Event-Based Alerts:
Problem: Alerts are event-based, not state-based.
Solution: Transition to a state-based alerting system that reflects the ongoing state rather than discrete events.

## Hardcoded Values:
Problem: Currently hardcoded thresholds (1 and 5) pose a critical issue.
Solution: Replace hardcoded values with dynamic configurations based on real-time data and testing feedback.
