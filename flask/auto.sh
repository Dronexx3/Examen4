#!/bin/bash
docker build -t flask-api .
docker run -d -it --network my-network -p 5000:5000 flask-api
