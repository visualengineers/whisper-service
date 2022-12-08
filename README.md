# Whisper Service

This is a small server to deliver [whisper](https://openai.com/blog/whisper/) speech to text.

# Prerequisites on the server

Docker must be installed on the system to deploy the server to an image.

# Development

## Python server

In order to test whisper locally on your system, you need to follow the steps on the [Whisper Github Page](https://github.com/openai/whisper):

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
$ docker build . -t visualengineers/whisper-service
$ docker run --name=whisper-server -d -p=5002:80 --restart always visualengineers/whisper-service
```

# Usage

Once you have the server running, either locally or as a Docker image, you need to provide POST requests to the route `/whisper`. Send a binary file as multipart parameter and form parameters to select the language model and language:

* uploaded_file: multipart, mimetype must be `audio/mpeg` or `audio/wav` or similar
* model: form parameter to specify the language model, can be {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large} – first usage of a model will lead to long waiting times because they need to be downloaded first
* language: form parameter to specify the used language, can by anything from: {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,hi,hr,ht,hu,hy,id,is,it,iw,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}

## Example

Using the [MultipartUtility](https://www.codejava.net/java-se/networking/upload-files-by-sending-multipart-request-programmatically), here is Java code to POST audio data to the service:

```Java
String url = "http://127.0.0.1:5002/whisper";
File binaryFile = new File("audio.mp3");
String result = "";

try {
    // See the MultipartUtility class in a seperate file for information
    MultipartUtility utility = new MultipartUtility(url, "UTF-8");
    utility.addHeaderField("Content-Type", "audio/mpeg");
    utility.addFilePart("uploaded_file", binaryFile);
    // We can choose different recognition  models: tiny, base, small, medium, large 
    utility.addFormField("model", "base");
    // We can recognize different languages, English (en) performs best, German (de) worse
    utility.addFormField("language", "de");
    List<String> response = utility.finish();
    for (String s : response)
        result += s;
} catch (IOException e) {
    e.printStackTrace();
}
```
