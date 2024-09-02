#!/bin/bash
docker build -t flask-api .
docker run -d --network=my_network -it --name flask-container -p 5000:5000 flask-api
