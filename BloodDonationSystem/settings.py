from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# FastAPI doesn't need a SECRET_KEY
DEBUG = True
ALLOWED_HOSTS = []

# Static and Media
STATIC_URL = '/static/'
# If you plan to serve media
MEDIA_ROOT = os.path.join(BASE_DIR, 'Donors/media')
MEDIA_URL = '/media/'


