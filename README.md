# Whisper Service

This is a small server to deliver [whisper](https://openai.com/blog/whisper/) speech to text.

# Prerequisites on the server

Docker must be installed on the system to deploy the server to an image.

# Development

## Python server

In order to test whisper locally on your system, you need to follow the steps on the [Whisker Github Page](https://github.com/openai/whisper):

* Install Python (at least version 3.7 or higher)

* Install ffmpeg, e.g.

```
sudo apt update && sudo apt install ffmpeg
```

* Install Whisper

```
pip install git+https://github.com/openai/whisper.git 
``` 

For the development of the server application, Python and pip are needed. The server is developed with flask. Dependencies can be installed using the `requirements.txt` file and pip:

```
pip install -r requirements.txt
```

See tutorials on developing a flask web server with python:

* https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/
* https://flask.palletsprojects.com/en/2.2.x/deploying/waitress/

Run the server locally either in development mode or in production (e.g. with waitress):

```
flask --app server run
waitress-serve --host 0.0.0.0 --port 5002 server:app
```

## Node server

There is an experimental node server for which you need to install Node.js and the required dependencies:

```
npm install express --save
npm install body-parser --save
npm install multer --save
```

To start the server, use the common command:

```
npm start
```

# Deployment

Build and deploy the Python web server version with the provided Docker file using the following commands:

```
docker build . -t kammer/whisper-service
docker run --name=whisper-server -d -p=5002:80 visualengineers/whisper-service
```