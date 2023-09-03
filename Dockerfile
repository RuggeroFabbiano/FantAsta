FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv
RUN python3 -m venv fantastenv

WORKDIR /code

# install dependencies
COPY requirements.txt /code/
RUN /fantastenv/bin/pip install -r requirements.txt

# Copy project
COPY . /code/

# Expose ports
EXPOSE 8000 

RUN chmod +x /code/start.sh
ENTRYPOINT ["./start.sh"]