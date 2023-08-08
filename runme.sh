#!/usr/bin/env bash

# Run docker and mount dev folder so you can edit and keep the container running

docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flaskapi