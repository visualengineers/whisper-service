from flask import Flask
from flask import request
from flask import render_template
import random
import string
import os

# define global variables
script_dir = os.path.dirname(os.path.realpath(__file__))
TMP_PATH = os.path.join(script_dir, 'tmp')

app = Flask(__name__)
whisperCommand = '/Users/kammer/opt/miniconda3/bin/whisper'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/whisper', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        contents = ''
        try:
            f = request.files['uploaded_file']
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
            letters = string.ascii_lowercase
            filename = ''.join(random.choice(letters) for i in range(32))
            extension = f.filename.split('.').pop()
            file = os.path.abspath(os.getcwd()) + '/tmp/'+filename+'.'+extension
            f.save(file)

            stream = os.popen(whisperCommand + ' ' + file + ' --model ' + model + ' --output_dir ./tmp --language ' + lang + ' --fp16 False')
            output = stream.read()
            with open(file + '.txt') as f:
                contents = f.read()
        except:
            print("An exception occured")
        finally:
            for file_name in os.listdir(TMP_PATH):
                # construct full file path
                file = os.path.join(TMP_PATH, file_name)
                if os.path.isfile(file) and file_name != '.gitkeep':
                    os.remove(file)

        return contents
    else:
        return render_template('whisper.html')