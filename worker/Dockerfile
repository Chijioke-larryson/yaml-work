#Base image
FROM python:3.8
#Working directory
WORKDIR /app
#Copy the dependencies file to the working directory
COPY  requirements.txt /requirements.txt

#Install the dependencies
RUN pip install --no-cache-dir -r /requirements.txt
#Copy the content of the local src directory to the working directory
COPY . .

#Command to run the application
CMD ["python", "worker.py"]

#Expose the port the app runs on
EXPOSE 80