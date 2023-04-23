# Note: this is the only image we need to upload, 
# celery is the same image but with different entrypoint
# the other services, postgres, redis, influx, etc are hosted in docker-hub
# as public images.

# gcloud auth login
# gcloud auth configure-docker

docker tag misw4204-grupo17-converter-web gcr.io/miso-mobile-2023/converter-web:1.2
docker push gcr.io/miso-mobile-2023/converter-web:1.2