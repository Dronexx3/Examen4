#!/bin/bash
docker build -t flask-api .
docker run -d -it -p 5000:5000 flask-api
