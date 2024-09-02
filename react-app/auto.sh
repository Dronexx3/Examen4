#!/bin/bash
docker build -t react-app .
docker run -d -it --network my-network -p 3001:80 react-app