FROM python:3
ENV TZ="Europe/Warsaw"
ENV APP_ROOT="/mqtt-to-graphite"

RUN mkdir -p /mqtt-to-graphite
RUN mkdir -p /mqtt-to-graphite/config
RUN mkdir -p /mqtt-to-graphite/logs

WORKDIR /mqtt-to-graphite

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/main/main.py"]
#CMD ["bash"]
