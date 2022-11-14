# Whisper Service
This is a small server to deliver [whisper](https://openai.com/blog/whisper/) speech to text.

# Prerequisites on the server

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
    * flask --app server run
    * waitress-serve --host 127.0.0.1 --port 5002 server:app
