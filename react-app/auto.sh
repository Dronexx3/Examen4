#!/bin/bash
docker build -t react-app .
docker run -d -it -p 3001:80 react-app