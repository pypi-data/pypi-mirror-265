# -*- coding: utf-8 -*-
import logging
from flask import Flask
import flask_request_id.log
import flask_request_id.utils

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/")
def hello():
    logger.info("Sending our hello")
    return "Hello World!"


if __name__ == "__main__":
    app.run()
