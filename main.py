import os
from flask import Flask, flash, render_template, request, session, redirect

# Static variables
APP_HOST = '127.0.0.1'
APP_PORT = 5000

# build the flask application
app = Flask(__name__)


@app.route('/')
def home():
    return "If you can see this, you've set up Flask!"


# Run the flask application
if __name__ == "__main__":
    #debug code
    app.secret_key = os.urandom(12)
    # run the application
    app.run(debug=True, host=APP_HOST, port=APP_PORT)