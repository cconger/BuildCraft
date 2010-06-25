from tipfy import RequestHandler, render_json_response, redirect_to, url_for, request, Response
from tipfy.ext.mako import render_response
from tipfy.ext.db import get_by_id_or_404, get_property_dict, populate_entity

from google.appengine.ext import db

from apps.buildcraft.helpers.sessionhandler import SessionHandler
from apps.buildcraft.models.gameVersion import GameVersion

class GameVersionIndexHandler(SessionHandler):
  def get(self, **kwargs):
    results = GameVersion.all().fetch(10)

    templateValues = {'gameVersions'  : results,
                      'create_url'    : url_for('version/create')}

    return self.render_page('game-versions.html', **templateValues)

class GameVersionCreateHandler(SessionHandler):
  def get(self, **kwargs):
    templateValues = {'title'           : 'Create Version',
                      'submit_url'      : url_for('version/create')}

    return self.render_page('game-version-form.html', **templateValues)

  def post(self, **kwargs):
    """Create"""
    newVersion = GameVersion()
    newVersion.version_number = request.form['versionNumber']
    newVersion.is_current = request.form.get('isCurrent', "No") == "Yes"

    if newVersion.is_current:
      current = GameVersion.getCurrent()
      if(current):
        current.is_current = False
        current.put()

    newVersion.put()
    return redirect_to('version/index')

class GameVersionDeleteHandler(SessionHandler):
  def get(self, **kwargs):
    version = db.get(kwargs['id'])
    version.delete()
    return redirect_to('version/index')

class GameVersionUpdateHandler(SessionHandler):
  def get(self, **kwargs):
    version = db.get(kwargs['id'])
    templateValues = {'title'        : 'Update Version',
                      'submit_url'   : url_for('version/update', id=kwargs['id']),
                      'existingVersion' : get_property_dict(version)}
    return self.render_page('game-version-form.html', **templateValues)

  def post(self, **kwargs):
    version = db.get(kwargs['id'])
    
    version.version_number = request.form.get('version_number')
    version.is_current = request.form.get('is_current', False, type=bool)

    if(version.is_current):
      current = GameVersion.getCurrent()
      if current and str(current.key()) is not str(version.key()) :
        current.is_current = False
        current.put()

    version.put()

    return redirect_to('version/index')

