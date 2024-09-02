#!/bin/bash
docker build -t webapi .
docker run -d -it -p 4000:4000 webapi