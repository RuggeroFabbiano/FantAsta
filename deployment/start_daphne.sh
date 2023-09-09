#!/bin/bash
source /fantastenv/bin/activate
cd /code

daphne -b 0.0.0.0 -p 8001 fantasta.asgi:application