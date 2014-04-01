
from time import sleep
import urllib2
import json
import threading
import yaml

# TODO probably just a json/http poller
class JenkinsPoller(threading.Thread):

  def __init__(self, build_monitor):
    threading.Thread.__init__(self)
    self.daemon = True
    self.build_monitor = build_monitor

  def run(self):
    poll = True
    while poll:
      sleep(3.0) # TODO config

      req = urllib2.Request('http://xcode-server.local:8080/api/json') # TODO config
      req.add_header('Content-Type', 'application/json')

      response_body = urllib2.urlopen(req).read()
      self.build_monitor.process_build( yaml.load(response_body) )
