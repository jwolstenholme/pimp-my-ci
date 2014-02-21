
import logging
from threading import Thread

log = logging.getLogger()

from time import sleep

pulsing = False

class Strand:

  def fill(self, r, g, b, start=0, end=0):
    log.info('StubStrand.fill')
    global pulsing
    pulsing = False

  def pulsate(self, r, g, b):
    log.info('StubStrand.pulsate')
    global pulsing
    if (pulsing): return

    pulsing = True

    worker = Thread(target=pulsate_strand, args=(r, g, b, ))
    worker.setDaemon(True)
    worker.start()

    log.info('StubStrand.pulsate EXIT!!!!!!!!!!!')

  def wheel(self, start=0, end=0):
    log.info('StubStrand.wheel')

def pulsate_strand(r, g, b):
  global pulsing
  while pulsing:
    log.info('pulsate_strand sleeping')
    sleep(5)
    log.info('pulsate_strand awake')
