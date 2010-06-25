from tipfy import RequestHandler, render_json_response, redirect_to, url_for, request, Response
from tipfy.ext.mako import render_response
from tipfy.ext.db import get_by_id_or_404, populate_entity, get_property_dict

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api.images import BadImageError, NotImageError

from apps.buildcraft.helpers.sessionhandler import SessionHandler

from apps.buildcraft.models.buildable import Buildable
from apps.buildcraft.models.race import Race
from apps.buildcraft.models.gameVersion import GameVersion

class BuildableIndexHandler(SessionHandler):
  def get(self, **kwargs):
    query = Buildable.all()
    results = query.fetch(10)

    templateValues = {'buildables'  : results,
                      'create_url'  : url_for('buildable/create')}

    return self.render_page('buildables.html', **templateValues)

class BuildableDetailHandler(SessionHandler):
  def get(self, **kwargs):
    pass

class BuildableCreateHandler(SessionHandler):
  def get(self, **kwargs):
    templateValues = {'title'           : 'Create Buildable',
                      'submit_url'      : url_for('buildable/create'),
                      'races'           : Race.all().fetch(10),
                      'gameVersions'    : GameVersion.all().fetch(10)}

    return self.render_page('buildable-form.html', **templateValues)

  def post(self, **kwargs):
    """Create"""
    image = request.files.get('image')
    if image:
      try:
        image = db.Blob(images.resize(image.read(), 64,64))
      except BadImageError, NotImageError:
        self.set_flash({'error' : "Error Processing Image"})
        return redirect_to('buildable/create')
    else:
      return redirect_to('buildable/create')

    name        = request.form.get('name')
    race        = db.get(request.form.get('race'))
    versions    = [db.Key(val) for val in request.form.getlist('game_versions')]
    description = request.form.get('description')
    
    costs = {}
    for cost in ('supply_cost', 'mineral_cost', 'gas_cost', 'energy_cost'):
      costValue = request.form.get(cost, type=int)
      if costValue:
        costs[cost] = costValue

    unit = Buildable(name=name,image=image,game_versions=versions,race=race,description=description, **costs)
    
    unit.put()

    if unit.key():
      self.set_flash({'success' : "Unit Successfully Created"})

    return redirect_to('buildable/index')

class BuildableDeleteHandler(SessionHandler):
  def get(self, **kwargs):
    entity = db.get(kwargs['id'])
    entity.delete()
    return redirect_to('version/index')

class BuildableUpdateHandler(SessionHandler):
  def get(self, **kwargs):
    buildable = db.get(kwargs['id'])
    templateValues = {'title'        : 'Update Unit',
                      'submit_url'   : url_for('buildable/update', id=kwargs['id']),
                      'races'           : Race.all(),
                      'gameVersions'    : GameVersion.all(),
                      'existingBuildable' : get_property_dict(buildable)}
    templateValues['existingBuildable']['imageUrl'] = buildable.imageUrl
    return self.render_page('buildable-form.html', **templateValues)

  def post(self, **kwargs):
    """Update"""
    unit               = get_by_id_or_404(Buildable, kwargs['id'])
    unit.name          = request.form.get('name')
    unit.race          = db.get(request.form.get('race'))
    unit.game_versions = [db.Key(val) for val in request.form.getlist('versions')]
    unit.description   = request.form.get('description', "")

    image = request.files.get('image')
    if image:
      try:
        unit.image = db.Blob(images.resize(image.read(), 64,64))
      except BadImageError, NotImageError:
        self.set_flash({'error' : "Error Processing Image"})
        return redirect_to('buildable/create')


    costs = {}
    for cost in ('supply_cost', 'mineral_cost', 'gas_cost', 'energy_cost'):
      costs[cost] = request.form.get(cost, type=int)

    populate_entity(unit, **costs)

    unit.put()

    session.set_flash_message({'success': "Update Completed Successfully"})

    return redirect_to('buildable/index')

class BuildableImageHandler(RequestHandler):
  def get(self, **kwargs):
    buildable = db.get(kwargs['id'])

    if buildable:
      headers = {'Content-Type' : 'image/png'}
      return Response(buildable.image, headers=headers)
    else:
      return redirect('/images/image_not_found.png')
