from flask import Flask
from app.routes import routes_bp

app = Flask(__name__)

# Register blueprint
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8005, debug=True)
