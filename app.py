from flask import Flask, render_template

app = Flask(__name__)

import config  # Ensure config is imported to load environment variables
import models  # Import models to register them with the app
import routes  # Import routes to register them with the app

if __name__ == '__main__':   
    app.run(debug=True) 