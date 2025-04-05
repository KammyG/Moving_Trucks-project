#!/bin/bash
gunicorn --workers 3 --bind 0.0.0.0:8000 moving_truck_api.wsgi:application
