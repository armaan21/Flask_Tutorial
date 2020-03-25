from flask import Flask

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

print(f'ENV is set to: {app.config["ENV"]}')

# app.config.from_object("config_filename.ConfigClass")
# app.config.from_object("config.ProductionConfig")

# import another python program views.py
from app import views
from app import admin_views