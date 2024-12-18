from flask import Flask
from app.routes.registration_routes import registration_bp

app = Flask(__name__)
app.register_blueprint(registration_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
