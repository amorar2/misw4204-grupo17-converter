FROM python:3.9-alpine

# Create app directory
WORKDIR /app
RUN apk update
RUN apk add --no-cache --virtual .build-deps \
    linux-headers build-base g++ python3-dev
COPY requirements.txt ./
ENV FLASK_APP=/app/api/app.py

RUN pip install -r requirements.txt

# Bundle app source
COPY . .


EXPOSE 5001
CMD [ "flask", "run","--host","0.0.0.0","--port","5001"]