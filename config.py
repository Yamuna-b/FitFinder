import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'db', 'uploads')
    OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'db', 'outputs')

    @staticmethod
    def ensure_dirs() -> None:
        for path in [Config.UPLOAD_FOLDER, Config.OUTPUT_FOLDER]:
            os.makedirs(path, exist_ok=True)


# Ensure directories exist during import in simple single-file run pattern
Config.ensure_dirs()


