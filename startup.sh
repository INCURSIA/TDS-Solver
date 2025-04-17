#!/bin/bash
apt-get update && apt-get install -y git
gunicorn -k uvicorn.workers.UvicornWorker main:app --bind=0.0.0.0:8000
