from tipfy import RequestHandler, render_json_response, redirect_to, url_for, request, Response
from tipfy.ext.mako import render_response
from tipfy.ext.db import get_property_dict

from google.appengine.api import images
from google.appengine.api.images import BadImageError, NotImageError
from google.appengine.ext import db

from apps.buildcraft.helpers.sessionhandler import SessionHandler
from apps.buildcraft.models.race import Race

class RaceIndexHandler(SessionHandler):
  """Race Indexer"""
  def get(self, **kwargs):
    query = Race.all()
    results = query.fetch(10)

    templateValues = {'races'  : results,
                      'create_url' : url_for('race/create')}

    return self.render_page('races.html', **templateValues)

class RaceCreateHandler(SessionHandler):
  def get(self, **kwargs):
    templateValues = {'title'           : 'Create Race',
                      'submit_url'      : url_for('race/create')}

    return self.render_page('race-form.html', **templateValues)

  def post(self, **kwargs):
    """Create"""
    raceName = request.form['name']
    letter = raceName[0]
    try:
      image = images.resize(request.files['image'].read(), 32,32)
    except BadImageError, NotImageError:
      #TODO: Should give another shot to correct...
      # Set Cookie with info, and flash message
      return redirect_to('race/index')
    newRace = Race(name = raceName, letter=letter, image=db.Blob(image))
    newRace.put()
    
    return redirect_to('race/index')

class RaceDeleteHandler(SessionHandler):
  def get(self, **kwargs):
    race = db.get(kwargs['id'])
    race.delete()
    return redirect_to('race/index')

class RaceUpdateHandler(SessionHandler):
  def get(self, **kwargs):
    race = db.get(kwargs['id'])
    templateValues = {'title'        : 'Update Race',
                      'submit_url'   : url_for('race/update', id=kwargs['id']),
                      'existingRace' : get_property_dict(race)}
    templateValues['existingRace']['imageUrl'] = race.imageUrl
    return self.render_page('race-form.html', **templateValues)

  def post(self, **kwargs):
    race = db.get(kwargs['id'])
    race.name = request.form['name']
    race.letter = race.name[0]
    if request.files['image']:
      try:
        race.image = db.Blob(images.resize(request.files['image'].read(), 32,32))
      except BadImageError, NotImageError:
        #TODO: Throw Flash Message
        return redirect_to('race/index')
        
    race.put()
    return redirect_to('race/index')

class RaceImageHandler(SessionHandler):
  def get(self, **kwargs):
    race = db.get(kwargs['id'])

    if race:
      headers = {'Content-Type' : 'image/png'}
      return Response(race.image, headers=headers)
    else:
      return redirect('/images/image_not_found.png')


