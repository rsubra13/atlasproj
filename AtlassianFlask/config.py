import os

DEBUG = True
CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
ADMIN = False
SECRET_KEY = 'you-will-never-guess'  # This is important.

# Database connection
SQLALCHEMY_DATABASE_URI = "postgresql://ramki:ramki@localhost/atlas"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')






