FROM python:3.9

# Setting home directory
ENV HOME /root

# Ensuring it's in main directory
WORKDIR /root

# Copy and install any project dependencies
COPY package*.json ./

# Copy all working files
COPY . .

RUN pip install -r requirements.txt

# Get port from Heroku
EXPOSE $PORT

# Run container
CMD python3 app.py $PORT