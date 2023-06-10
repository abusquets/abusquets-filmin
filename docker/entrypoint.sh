#!/bin/bash

set -e

case $1 in

    run-devel)
        echo "→ Running as development mode"
        DEBUGPY="${DEBUGPY:-false}"
        exec bash -c 'if [ "${DEBUGPY}" == "True" ]; then python -m debugpy --listen 0.0.0.0:5678 -m uvicorn app.asgi:app --host 0.0.0.0 --port 80 --reload --reload-dir /app; else python -m uvicorn app.asgi:app --host 0.0.0.0 --port 80 --reload --reload-dir /app; fi'
        ;;

    run-asgi)
        echo "→ Running as prod mode"
        exec gunicorn app.asgi:app --workers 5 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
        ;;

    *)
        exec "$@"
        ;;
esac
