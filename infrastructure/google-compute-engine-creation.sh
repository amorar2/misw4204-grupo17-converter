## Set up flask-api
gcloud compute instances create-with-container flask-api3 \
    --project=miso-mobile-2023 \
    --zone=us-east1-b \
    --machine-type=e2-micro \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=371641758004-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
    --image=projects/cos-cloud/global/images/cos-stable-105-17412-1-66 \
    --boot-disk-size=10GB \
    --boot-disk-type=pd-balanced \
    --boot-disk-device-name=flask-api3 \
    --container-image=gcr.io/miso-mobile-2023/converter-web:1.3 \
    --container-restart-policy=always \
    --container-command=flask \
    --container-arg=run \
    --container-arg=--host=0.0.0.0 \
    --container-arg=-p\ \
5001 \
    --container-env=DATABASE_URL=postgresql://postgres:postgres@34.23.114.143:5432/converter \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=ec-src=vm_add-gcloud,container-vm=cos-stable-105-17412-1-66

## Set up redis instance
gcloud compute instances create-with-container redis \
--project=miso-mobile-2023 \
--zone=us-east1-b \
--machine-type=e2-micro \
--network-interface=network-tier=PREMIUM,subnet=default \
--maintenance-policy=MIGRATE \
--provisioning-model=STANDARD \
--service-account=371641758004-compute@developer.gserviceaccount.com \
--scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
--image=projects/cos-cloud/global/images/cos-stable-105-17412-1-66 \
--boot-disk-size=10GB \
--boot-disk-type=pd-balanced \
--boot-disk-device-name=redis \
--container-image=redis:6.0 \
--container-restart-policy=always \
--container-command=redis-server \
--no-shielded-secure-boot \
--shielded-vtpm \
--shielded-integrity-monitoring \
--labels=ec-src=vm_add-gcloud,container-vm=cos-stable-105-17412-1-66