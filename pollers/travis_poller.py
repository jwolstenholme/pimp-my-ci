
import urllib2
from http_json_poller import HttpJsonPoller

class TravisPoller(HttpJsonPoller):

  def create_request(self, job):
    return urllib2.Request(job.url, headers={"Accept" : "application/vnd.travis-ci.2+json"})
