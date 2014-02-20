
from time import sleep
import urllib2
import json
import yaml

# TODO probably just a json/http poller
class JenkinsPoller:

  def __init__(self, build_monitor):
    self.build_monitor = build_monitor

  def start(self):
    while True:
      sleep(3.0) # TODO config

      req = urllib2.Request('http://xcode-server.local:8080/api/json') # TODO config
      req.add_header('Content-Type', 'application/json')

      response_body = urllib2.urlopen(req).read()
      self.build_monitor.process_build( yaml.load(response_body) )
