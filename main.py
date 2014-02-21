# script expects RPI_HOME to be set as an env var

import sys
import os
import logging

from lights_controller import LightsController
from monitors.jenkins_monitor import JenkinsMonitor
from pollers.jenkins_poller import JenkinsPoller

logging.basicConfig(level=logging.INFO,
    filename="{0}/logs/pipeline.log".format(os.environ['RPI_HOME']),
    format="%(asctime)s <%(threadName)s>: %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger()

def main():

    while True:
        # TODO config
        jobs = ['Truman']
        lights_controller = LightsController(jobs)
        try:
            # start polling jenkins
            build_monitor = JenkinsMonitor(jobs, lights_controller)
            JenkinsPoller(build_monitor).start()
        except KeyboardInterrupt:
            log.info('^C received, shutting down controller')
            lights_controller.off()
            sys.exit()

if __name__ == '__main__':
    main()
