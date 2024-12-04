FROM python:3.10-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y  \   
postgresql-client \
gdal-bin \
binutils \
libproj-dev \
proj-data \
libgdal-dev \ 
&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
