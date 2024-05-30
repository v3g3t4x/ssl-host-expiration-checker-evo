pip install validators
pip install -U colorama
pip install -U dnspython
pip install -U requests


docker run --name ssl-checker-redis -p 6379:6379 -d redis:7.0.15-alpine3.20


py app.py

http://127.0.0.1:5000/