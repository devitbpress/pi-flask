from flask import Flask
from app.routes import routes_bp
from app.api import routes_api

app = Flask(__name__)

# Register blueprint
app.register_blueprint(routes_bp)
app.register_blueprint(routes_api)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
