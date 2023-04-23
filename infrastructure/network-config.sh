# Set up firewall rule to allow inbound traffic to redis TCP port
gcloud compute --project=miso-mobile-2023 firewall-rules create redis --description="redis connection" --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:6379 --source-ranges=0.0.0.0/0

# Set up firewall rule to allow inbound traffic to flask api
gcloud compute --project=miso-mobile-2023 firewall-rules create redis --description="flask api" --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:5001 --source-ranges=0.0.0.0/0