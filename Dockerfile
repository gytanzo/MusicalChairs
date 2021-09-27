FROM python3

# Setting home directory
ENV HOME /MusicalChairs

# Ensuring it's in main directory
WORKDIR /MusicalChairs

# Copy and install any project dependencies
COPY package*.json ./

RUN npm install

# Get port from Heroku
EXPOSE $PORT

# Copy all working files
COPY . .

# Run container
CMD python3 app.py $PORT