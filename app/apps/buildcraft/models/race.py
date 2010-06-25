from google.appengine.ext import db
from tipfy import url_for

class Race(db.Model):
  name = db.StringProperty(required=True)
  letter = db.StringProperty(required=True)
  image = db.BlobProperty(required=True)

  @property
  def updateUrl(self):
    return url_for('race/update', id=self.key())

  @property
  def deleteUrl(self):
    return url_for('race/delete', id=self.key())

  @property
  def imageUrl(self):
    return url_for('race/image', id=self.key())

  @property
  def createUrl(self):
    return url_for('race/create')

  @classmethod
  def getRaceByName(cls, name, defaultValue=None):
    result = db.GqlQuery("SELECT * FROM Race WHERE name = :1 LIMIT 1", name).fetch(1)
    if(len(result) > 0):
      return result[0]
    else:
      return defaultValue
