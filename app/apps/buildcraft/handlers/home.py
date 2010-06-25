from tipfy import RequestHandler, render_json_response, redirect_to, url_for, request, Response
from tipfy.ext.mako import render_response

from google.appengine.api import images
from google.appengine.api.images import BadImageError, NotImageError
from google.appengine.ext import db

from apps.buildcraft.models.race import Race

class MainPage(RequestHandler):
  def get(self, **kwargs):
    return render_response('index.html')

