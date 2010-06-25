# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE.txt for more details.
"""
from tipfy import Rule


def get_rules():
    """Returns a list of URL rules for the Hello, World! application."""
    rules = [
        ##MAIN PAGE
        Rule('/', endpoint='home', handler='apps.buildcraft.handlers.home.MainPage'),

        ##VERSIONS
        Rule('/versions', endpoint='version/index', handler='apps.buildcraft.handlers.gameversion.GameVersionIndexHandler'),
        Rule('/version/new', endpoint='version/create', handler='apps.buildcraft.handlers.gameversion.GameVersionCreateHandler'),
        Rule('/version/<id>/edit', endpoint='version/update', handler='apps.buildcraft.handlers.gameversion.GameVersionUpdateHandler'),
        Rule('/version/<id>/del', endpoint='version/delete', handler='apps.buildcraft.handlers.gameversion.GameVersionDeleteHandler'),

        ##BUILDABLES
        Rule('/units', endpoint='buildable/index', handler='apps.buildcraft.handlers.buildable.BuildableIndexHandler'),
        Rule('/unit/<id>', endpoint='buildable/detail', handler='apps.buildcraft.handlers.buildable.BuildableDetailHandler'),
        Rule('/unit/new', endpoint='buildable/create', handler='apps.buildcraft.handlers.buildable.BuildableCreateHandler'),
        Rule('/unit/image/<id>.png', endpoint='buildable/image', handler='apps.buildcraft.handlers.buildable.BuildableImageHandler'),
        Rule('/unit/<id>/edit', endpoint='buildable/update', handler='apps.buildcraft.handlers.buildable.BuildableUpdateHandler'),
        Rule('/unit/<id>/del', endpoint='buildable/delete', handler='apps.buildcraft.handlers.buildable.BuildableDeleteHandler'),
        ##RACES
        Rule('/races', endpoint='race/index', handler='apps.buildcraft.handlers.race.RaceIndexHandler'),
        Rule('/race/new', endpoint='race/create', handler='apps.buildcraft.handlers.race.RaceCreateHandler'),
        Rule('/race/image/<id>.png', endpoint='race/image', handler='apps.buildcraft.handlers.race.RaceImageHandler'),
        Rule('/race/<id>/edit', endpoint='race/update', handler='apps.buildcraft.handlers.race.RaceUpdateHandler'),
        Rule('/race/<id>/del', endpoint='race/delete', handler='apps.buildcraft.handlers.race.RaceDeleteHandler'),
    ]

    return rules
