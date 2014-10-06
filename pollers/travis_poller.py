
from pollers.http_json_poller import HttpJsonPoller

class TravisPoller(HttpJsonPoller):

  def customise_request(self, request):
    request.add_header('Content-Type', 'application/vnd.travis-ci.2+json')
