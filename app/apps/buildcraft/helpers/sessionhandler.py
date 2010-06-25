from tipfy import RequestHandler, render_json_response, redirect_to, url_for, request, Response
from tipfy.ext.mako import render_response
from tipfy.ext.session import SessionMiddleware, SessionMixin

class SessionHandler(RequestHandler, SessionMixin):
  #This list enables middleware for the handler
  middleware = [SessionMiddleware]

  def render_page(self, target, **targetContext):
    targetContext['__fm'] = self.get_flash()

    return render_response(target, **targetContext)


