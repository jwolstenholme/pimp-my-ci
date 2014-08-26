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
from lib.build_job import BuildJob
from lib.lights_controller import LightsController
from lib.sounds_controller import SoundsController
from monitors.jenkins_monitor import JenkinsMonitor
from pollers.http_json_poller import HttpJsonPoller

logging.basicConfig(
    level=logging.INFO,
    filename="{0}/logs/pimpmyci.log".format(os.environ['RPI_HOME']),
    format="%(asctime)s <%(threadName)s>: %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p',
    maxBytes=1024,
    backupCount=3)
log = logging.getLogger()

def worker(controllers, job, queue):
  while True:
    try:
        status = queue.get_nowait()
        for controller in controllers:
            controller.update_build_status(job, status)
        queue.task_done()
    except Queue.Empty:
        sleep(1)

class PimpMyCi:

    running = True

    def __init__(self, led_strip):
        jobs = BuildJob.from_dictionaries(Config.jobs)
        job_names = [ job.name for job in jobs ]

        sounds_controller = SoundsController(job_names)
        lights_controller = LightsController(led_strip, jobs)
        lights_controller.off()

        # start polling jenkins
        job_queues = { job: Queue.Queue() for job in jobs }
        build_monitor = JenkinsMonitor(job_queues)
        HttpJsonPoller(build_monitor).start()

        controllers = list( (lights_controller, sounds_controller) )

        for job, queue in job_queues.iteritems():
            t = Thread(target=worker, args=(controllers, job, queue, ))
            t.daemon = True
            t.start()

    def start(self):
        while self.running:
            try:
                sleep(0.05)
            except KeyboardInterrupt:
                log.info('^C received, shutting down controller')
                lights_controller.off()
                sys.exit()
            except:
                log.error("Unexpected error: %s", sys.exc_info()[0])
                log.error(traceback.format_exc())
                lights_controller.error()

    def stop(self):
        self.running = False

def main():
    led_strip = LEDStrip(Config.total_number_leds)
    PimpMyCi(led_strip).start()

if __name__ == '__main__':
    main()
