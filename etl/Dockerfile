# OS Image
# FROM ubuntu
FROM python

# Contact details
LABEL maintainer="Abdullah Reza"
LABEL contact_email="air.reza@hotmail.com"

# Update and upgrade the image
# RUN apt update && apt upgrade -y
# RUN apt auto-remove

# Install python & pip
# RUN apt install python3 -y
# RUN apt install python3-pip -y

# Set working directory
WORKDIR /usr/src/etl_app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip3 install -r requirements.txt

# Add etl script
ADD ./etl.py ./etl/etl.py

# Run the script
CMD ["python3", "./etl/etl.py"]