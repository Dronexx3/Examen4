#!/bin/bash
docker build -t react-app .
docker run -d -it --name react-container -p 3001:80 react-app