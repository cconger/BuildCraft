from google.appengine.ext import db
from tipfy.ext.auth.model import User

class BuildOrder(db.Model):
  name          = db.StringProperty(required=True)
  author        = User()
  created       = db.DateTimeProperty(auto_now_add = True)
  updated       = db.DateTimeProperty(auto_now = True)
  description   = db.StringProperty(multiline=True)
  game_versions = db.ListProperty(db.Key)

