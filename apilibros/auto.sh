#!/bin/bash
docker build -t webapi .
docker run -d --network=my_network -it --name csharp-container -p 4000:4000 webapi