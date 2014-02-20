# script expects RPI_HOME to be set as an env var

import sys
import os
import Queue
import logging
from time import sleep

from lights_controller import LightsController
from unrecognised_directive_exception import UnrecognisedDirective
from monitors.jenkins_monitor import JenkinsMonitor
from pollers.jenkins_poller import JenkinsPoller

logging.basicConfig(level=logging.INFO,
    filename="{0}/logs/pipeline.log".format(os.environ['RPI_HOME']),
    format="%(asctime)s <%(threadName)s>: %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger()

def main():

    directive_buffer = current_directive = 'all_off'
    play_sound = False

    while True:
        try:
            # TODO config
            jobs = ['Truman']

            # start polling jenkins
            lights_controller = LightsController(jobs)
            build_monitor = JenkinsMonitor(jobs, lights_controller)
            JenkinsPoller(build_monitor).start()

        except UnrecognisedDirective:
            log.error('bad directive received.. reverting to buffered directive..')
            current_directive = directive_buffer
            play_sound = False

        except Queue.Empty:
            sleep(0.03) # loop fast enough for animations ---> this could be altered per directive if reqd

        except KeyboardInterrupt:
            log.info('^C received, shutting down controller')
            translator.issue_directive('all_off')
            sys.exit()

if __name__ == '__main__':
    main()
