FROM python:3.10-slim
WORKDIR app
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]