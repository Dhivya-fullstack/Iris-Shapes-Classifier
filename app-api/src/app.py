import connexion
from flask import Flask

# Create Connexion app
app = connexion.App(__name__, specification_dir='./')

# Add API from OpenAPI spec
app.add_api("openapi.yaml")

# Access the underlying Flask app
flask_app = app.app

@flask_app.route('/', methods=['GET'])
def hello():
    return "Server is running!"

@flask_app.get("/api/models/shapesClassifier")
def shapes_classifier_get():
    return {"message": "API is working! Use PUT to send image."}


if __name__ == "__main__":
    app.run(port=8002)