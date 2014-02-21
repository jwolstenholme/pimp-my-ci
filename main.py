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
        try:
            # TODO config
            jobs = ['Truman']

            # start polling jenkins
            lights_controller = LightsController(jobs)
            build_monitor = JenkinsMonitor(jobs, lights_controller)
            JenkinsPoller(build_monitor).start()

        except KeyboardInterrupt:
            log.info('^C received, shutting down controller')
            # TODO translator.issue_directive('all_off')
            sys.exit()

if __name__ == '__main__':
    main()
