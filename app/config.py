class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "C:/Users/armaa/OneDrive/Desktop/PDF2Audio/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True

# config class we use for running in production
# pass --> inherits from parent class
class ProductionConfig(Config):
    pass

# config class we use for development
class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "C:/Users/armaa/OneDrive/Desktop/PDF2Audio/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False

# config class we use for testing
class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False