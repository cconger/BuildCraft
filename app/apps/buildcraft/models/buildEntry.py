from google.appengine.ext import db

class BuildEntry(db.Model):
  supply_quota  = db.IntegerProperty()
  mineral_quota = db.IntegerProperty()
  gas_quota     = db.IntegerProperty()
  energy_quota  = db.IntegerProperty()
  buildable     = db.ReferenceProperty(required=True)
  comment       = db.StringProperty(multiline=True)
