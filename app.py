# flask-flasgger-example/app.py
# -*- coding: utf-8 -*-

import json
from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
app.config["SWAGGER"] = {"title": "Greetings API"}
db = json.load(open("greetings.json"))
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apisec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}

swagger = Swagger(
    app,
    template={
        "swaggerUiPrefix": LazyString(lambda: request.environ.get("SCRIPT_NAME", ""))
    },
    config=swagger_config
)


@app.route("/greetings/")
def list():
    """Example endpoint return all known greetings
    This is using docstring for specifications
    ---
    tags:
      - greetings
    operationId: list_greetings
    consumes:
      - application/jsont
    produces:
      - application/json
    security:
      greetings_auth:
        - 'read:greetings'
    schemes: ['http', 'https']
    deprecated: false
    responses:
      200:
        description: All known greetings
        examples:
        - ["Hello", "هَبَارِ"]
    """
    return jsonify([{"lang": lang, "text": text} for lang, text in sorted(db.items())])


@app.route("/greetings/<lang>/")
def get(lang):
    """Example endpoint return a greeting by language
    This is using docstring for specifications
    ---
    tags:
      - greetings
    parameters:
      - name: lang
        in: path
        type: string
        required: true
        default: en
        description: A greeting in which language?
    operationId: get_greetings
    consumes:
      - application/json
    produces:
      - application/json
    security:
      greetings_auth:
        - 'read:greetings'
    schemes: ['http', 'https']
    deprecated: false
    responses:
      200:
        description: The greeting for the given language
        examples:
          en: Hello
    """
    return jsonify({"lang": lang, "text": db.get(lang)})