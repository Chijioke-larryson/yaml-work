#python base image 
FROM python:3.8-slim
# set the working directory in the container
WORKDIR /app
# copy the dependencies file to the working directory
COPY requirements.txt /requirements.txt
# install the dependencies
RUN pip install --no-cache-dir -r /requirements.txt
# copy the content of the local src directory to the working directory
COPY . .
#Staging the port the app runs on
CMD ["python", "app.py"]

#Expose the port the app runs on
EXPOSE 80