from flask import Flask, render_template
import redis
#import os

app = Flask(__name__)

# Conectarse a Redis
redis_host = 'redis'
redis_port = 6379
# redis_host = os.environ.get('REDIS_HOST', 'localhost')
# redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/')
def index():
    # Increment visit counter
    visits = redis_client.incr('visits')
    return render_template('index.html', visits=visits)
