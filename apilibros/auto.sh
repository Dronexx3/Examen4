#!/bin/bash
docker build -t webapi .
docker run -d -it --network my-network -p 4000:4000 webapi