#!/usr/bin/python3
"""
Views module for API version 1
"""

from flask import Blueprint

# Create a Blueprint instance for API version 1
app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")

# Import views for different endpoints
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.users import *
from api.v1.views.places_amenities import *

