#!/bin/bash
echo "Starting script"
rm logs.txt
touch logs.txt
docker stop udemy-tutorial-container >>logs.txt
docker rm udemy-tutorial-container >>logs.txt
docker build -t udemy-tutorial app/ >>logs.txt
# docker run --name udemy-tutorial-container udemy-tutorial >>logs.txt
docker run -d -p 5000:5000 -w /app -v "$PWD/app:/app" --name udemy-tutorial-container udemy-tutorial >>logs.txt
exit 0