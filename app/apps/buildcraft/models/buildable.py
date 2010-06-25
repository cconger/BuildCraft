from google.appengine.ext import db
from tipfy import url_for

class Buildable(db.Model):
  name          = db.StringProperty(required=True)
  image         = db.BlobProperty(required=True)
  supply_cost   = db.IntegerProperty()
  mineral_cost  = db.IntegerProperty()
  gas_cost      = db.IntegerProperty()
  energy_cost   = db.IntegerProperty()
  game_versions = db.ListProperty(db.Key)
  race          = db.ReferenceProperty(required=True)
  description   = db.StringProperty(multiline=True)

  @property
  def createUrl(self):
    return url_for('buildable/create')

  @property
  def updateUrl(self):
    return url_for('buildable/update', id=self.key())

  @property
  def deleteUrl(self):
    return url_for('buildable/create', id=self.key())

  @property
  def detailUrl(self):
    return url_for('buildable/detail', id=self.key())

  @property
  def imageUrl(self):
    return url_for('buildable/image', id=self.key())
