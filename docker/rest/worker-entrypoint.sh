#!/bin/sh

until cd /app/rest
do
    echo "Waiting for server volume..."
done

# run a worker
celery -A rest worker --loglevel=info --concurrency 1 -E -B
