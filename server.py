from flask import Flask
from flask_cors import CORS
from flask import request
from flask import render_template
import random
import string
import os
import speech_recognition as sr

# define global variables
script_dir = os.path.dirname(os.path.realpath(__file__))
TMP_PATH = os.path.join(script_dir, 'tmp')

app = Flask(__name__)
CORS(app)

whisperCommand = os.getenv('WHISPER_PATH')

def saveFile(f):
    letters = string.ascii_lowercase
    filename = ''.join(random.choice(letters) for i in range(32))
    extension = f.filename.split('.').pop()
    file = TMP_PATH + '/' +  filename + '.' + extension
    f.save(file)
    return file

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# https://github.com/Uberi/speech_recognition/
@app.route('/google', methods=['GET', 'POST'])
def google():
    if request.method == 'POST':
        file = saveFile(request.files['uploaded_file'])

        # use the audio file as the audio source
        r = sr.Recognizer()
        with sr.AudioFile(file) as source:
            audio = r.record(source)  # read the entire audio file

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            transcript = r.recognize_google(audio)
            print(transcript)
            return transcript
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e)
    else:
        return render_template('google.html')
    
# https://flask.palletsprojects.com/en/2.2.x/quickstart/
@app.route('/whisper', methods=['GET', 'POST'])
def whisper():
    if request.method == 'POST':
        contents = ''
        try:
            model = 'tiny'
            if 'model' in request.form.keys():
                model = request.form['model'].strip()
            if model == '':
                model = 'tiny'
            lang = 'de'
            if 'language' in request.form.keys():
                lang = request.form['language'].strip()
            if lang == '':
                lang = 'de'
            if not('audio' in f.mimetype):
                return "Error Filetype"
            
            file = saveFile(request.files['uploaded_file'])
            resultFile = file + '.txt'

            stream = os.popen(whisperCommand + ' ' + file + ' --model ' + model + ' --output_dir ' + TMP_PATH + ' --language ' + lang + ' --output_format txt' + ' --fp16 False')
            output = stream.read()
            print(output)

            # https://www.pythontutorial.net/python-basics/python-read-text-file/
            with open(resultFile) as f:
                contents = f.read()
        except:
            print("An exception occured")
            contents = 'Server Error'
        finally:
            # https://pynative.com/python-delete-files-and-directories/#h-delete-all-files-from-a-directory
            for file_name in os.listdir(TMP_PATH):
                # construct full file path
                file = os.path.join(TMP_PATH, file_name)
                if os.path.isfile(file) and file_name != '.gitkeep':
                    os.remove(file)

        return contents
    else:
        return render_template('whisper.html')