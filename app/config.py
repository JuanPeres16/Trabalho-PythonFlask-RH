import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    APP_NAME = os.getenv("APP_NAME", "PeopleFlow")
    SECRET_KEY = os.getenv("SECRET_KEY", "peopleflow-secret-key")

    MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "peopleflow")
    MYSQL_USER = os.getenv("MYSQL_USER", "peopleflow_user")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "peopleflow_password")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
            f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        ),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/peopleflow_logs")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "employees")
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
