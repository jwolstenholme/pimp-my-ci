# script expects RPI_HOME to be set as an env var

import sys
import os
import logging
import threading
import traceback
import Queue

from time import sleep
from threading import Thread
from lib.config import Config
from lib.ledstrip import LEDStrip
from lib.build_jobs import BuildJobs
from lib.lights_controller import LightsController
from lib.sounds_controller import SoundsController

logging.basicConfig(
    level=logging.INFO,
    filename="{0}/logs/pimpmyci.log".format(os.environ['RPI_HOME']),
    format="%(asctime)s <%(threadName)s>: %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p',
    maxBytes=1024,
    backupCount=3)
log = logging.getLogger()

class PimpMyCi:

    running = True

    def __init__(self, led_strip):
        #jobs is an instance of BuildJobs
        jobs = BuildJobs.from_dictionaries(Config.platform, Config.job_defaults, Config.jobs)

        sounds_controller = SoundsController(jobs.names)
        lights_controller = LightsController(led_strip, jobs)
        lights_controller.off()

        controllers = list( (lights_controller, sounds_controller) )
        jobs.start_polling(controllers)

    def start(self):
        while self.running:
            try:
                sleep(0.05)
            except KeyboardInterrupt:
                log.info('^C received, shutting down controller')
                lights_controller.off()
                sys.exit()
            except Exception as e:
                log.error("Unexpected error type: %s", type(e))
                log.error("Unexpected error args: %s", e.args)
                lights_controller.error()

    def stop(self):
        self.running = False

def main():
    led_strip = LEDStrip(Config.total_number_leds)
    PimpMyCi(led_strip).start()

if __name__ == '__main__':
    main()
