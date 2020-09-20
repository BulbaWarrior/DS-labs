# Specify base image
FROM python:3.7

# Copy particular file
COPY requirements.txt /tmp/

# Execute commands inside the container, so that you can customize it
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Create and cd to this directory, set default command to run container
WORKDIR /app

#Copy files from project dir into container's folder
COPY ./index.html /app
COPY ./main.py /app

# Specify port that could(!) be opened from container later
Expose 8080
#CMD python main.py


