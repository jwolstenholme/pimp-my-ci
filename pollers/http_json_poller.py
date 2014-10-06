
from time import sleep
import logging
import sys
import threading
import urllib2
import yaml

from lib.config import Config

log = logging.getLogger()

class HttpJsonPoller(threading.Thread):

  def __init__(self, url, build_monitor):
    threading.Thread.__init__(self)
    self.daemon = True
    self.build_monitor = build_monitor
    self.url = url

  def run(self):
    poll = True
    while poll:
      sleep(Config.polling_interval_secs)

      try:
        req = urllib2.Request(self.url)
        self.customise_request(req)

        response_body = urllib2.urlopen(req).read()
        self.build_monitor.process_build( yaml.load(response_body) )
      except:
        self.build_monitor.error()
        log.error( "HttpJsonPoller error: %s", sys.exc_info()[0] )

  def customise_request(self, request):
    request.add_header('Content-Type', 'application/json')

