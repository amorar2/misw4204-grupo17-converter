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

#Create NFS server
gcloud compute instances create nfs-server \
    --project=miso-mobile-2023 \
    --zone=us-east1-b \
    --machine-type=e2-micro \
    --image-project ubuntu-os-cloud \
    --image-family ubuntu-2004-lts \
    --boot-disk-size 10GB \
    --tags nfs-server \

gcloud compute instances create nfs-client \
    --project=miso-mobile-2023 \
    --zone=us-east1-b \
    --machine-type=e2-micro \
    --image-project ubuntu-os-cloud \
    --image-family ubuntu-2004-lts \
    --boot-disk-size 10GB \
    --tags nfs-client \


#Celery setup
gcloud compute instances create flask-celery \
    --project=miso-mobile-2023 \
    --zone=us-east1-b \
    --machine-type=e2-micro \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --metadata=^,@^ssh-keys=miso_mobile2023:ecdsa-sha2-nistp256\ \
AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBHA8NWA5GEcYNMNFZSKCx/2hNMkpU/5dmbiAlUt7IeT8MdvdzfI3tZRe\+SSqBCZclI6o8X\+bqAOPcIIWfLdtHJ8=\ google-ssh\ \{\"userName\":\"miso.mobile2023@gmail.com\",\"expireOn\":\"2023-04-24T03:09:05\+0000\"\}$'\n'miso_mobile2023:ssh-rsa\ AAAAB3NzaC1yc2EAAAADAQABAAABAQCJONHbb1nhFCTmzkwMw4oa370wn6rbKNdD3zC9ngFkSLkwFB5khx0NKg\+\+N6Eb8Z581lJ9VyXnJZs8Qtan65UaWJguEbF8iqMudvF98L1FpAyOPNpSZUHvnOacKTphvzI9JgmxWBloyzNMZKcvLJ2O1c\+m6mkT8fQRz6laU7auuUarRVOiDn/7PSSB8TkOD/BCyENDCJ4BwCml5cHYq8MPJJ1Eeop82Ov1aZzBTt6ZUuobfEoIkMGtbdbsiGijIuLTcAn7jKeTzuN72Br/BSQCvzFM2VhCyyfkwqJ6o4Yp\+F/qQgLTnk0QP2Dxx5xwc9zVY1tfVhcqryFUTgZvHbGj\ google-ssh\ \{\"userName\":\"miso.mobile2023@gmail.com\",\"expireOn\":\"2023-04-24T03:09:20\+0000\"\} \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=371641758004-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
    --min-cpu-platform=Automatic \
    --tags=nfs-client \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=ec-src=vm_add-gcloud \
    --reservation-affinity=any \
    --source-machine-image=flask-celery