# app/assets/__init__.py

from flask import Blueprint

asset = Blueprint('assets', __name__)

from . import views

