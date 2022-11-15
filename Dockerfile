FROM python:3
WORKDIR /app

RUN apt update -y && apt install ffmpeg -y
RUN pip install git+https://github.com/openai/whisper.git 

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 80

CMD [ "waitress-serve", "--host", "0.0.0.0", "--port", "80", "server:app" ]