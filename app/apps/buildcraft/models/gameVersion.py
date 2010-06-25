from google.appengine.ext import db

from tipfy import url_for

class GameVersion(db.Model):
  version_number = db.StringProperty()
  is_current = db.BooleanProperty()
  date_added = db.DateTimeProperty(auto_now_add=True)

  @property
  def createUrl(self):
    return url_for('version/create')

  @property
  def updateUrl(self):
    return url_for('version/update', id=self.key())

  @property
  def deleteUrl(self):
    return url_for('version/delete', id=self.key())

  @classmethod
  def getCurrent(cls, default_value=None):
    q = GameVersion.all()
    q.filter("is_current =", True)

    current = q.fetch(1)
    if len(current) > 0:
      return current[0]
    else:
      return default_value

