FROM python:3.9-slim

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl 

RUN ls 
RUN pip3 install -r requirements.txt
RUN pip3 install -e . 

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Mortgage_Calculator.py", "--server.port=8501", "--server.address=0.0.0.0"]