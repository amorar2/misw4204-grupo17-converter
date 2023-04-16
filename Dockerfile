FROM python:3.9-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./
ENV FLASK_APP=/app/api/app.py

RUN pip install -r requirements.txt

# Bundle app source
COPY . .


EXPOSE 5001
CMD [ "flask", "run","--host","0.0.0.0","--port","5001"]