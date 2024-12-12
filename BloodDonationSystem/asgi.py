import os
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

# Import your FastAPI app
from fastapi_app import app as fastapi_app  # Assuming fastapi_app.py contains 'app = FastAPI()'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BloodDonationSystem.settings")

# For FastAPI, we do not need the Django ASGI application anymore
application = fastapi_app
