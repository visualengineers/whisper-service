# Whisper Service

This is a small server to deliver [whisper](https://openai.com/blog/whisper/) speech to text.

# Prerequisites on the server

Docker

## Install Whisper as command line tool

Follow the instructions on the [Whisker Github Page](https://github.com/openai/whisper).

* Install Python (at least version 3.7 or higher)

* Install ffmpeg, e.g.

```
sudo apt update && sudo apt install ffmpeg
```

* Install Whisper, e.g.

```
pip install git+https://github.com/openai/whisper.git 
``` 
/usr/local/python/
## Install flask

```
pip install flask
```

## Install Node.js

* Install express and dependencies

```
npm install express --save
npm install body-parser --save
npm install multer --save
```

# Run the server

* Node server: npm start
* Python server: 
    * https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/
    * https://flask.palletsprojects.com/en/2.2.x/deploying/waitress/
    * flask --app server run
    * waitress-serve --host 0.0.0.0 --port 5002 server:app

* docker build . -t kammer/whisper-service
* docker run --name=whisper-server -p=5002:80 kammer/whisper-service