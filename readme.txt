docker run -d -p 5000:5000 -w /app -v "$PWD:/app" --name udemy-tutorial-container udemy-tutorial

Syncs current folder to the folder in container. i.e creates a volume
Enables automatic reloading inside the container