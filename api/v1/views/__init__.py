#!/usr/bin/python3
"""
__init__ creates Blueprint instance with `url_prefix` set to `/api/v1`.
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import index_function
from api.v1.views.states import StateView
from api.v1.views.cities import CityView
from api.v1.views.amenities import AmenityView
from api.v1.views.users import UserView
from api.v1.views.places import PlaceView
from api.v1.views.places_reviews import PlaceReviewView
from api.v1.views.places_amenities import PlaceAmenityView
