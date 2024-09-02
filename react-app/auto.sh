#!/bin/bash
docker build -t react-app .
docker run -d --network=my_network -it --name react-container -p 3001:80 react-app