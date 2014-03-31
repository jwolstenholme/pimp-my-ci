# script expects RPI_HOME to be set as an env var

import sys
import os
import logging
import traceback

from time import sleep
from lib.const import *

from lib.ledstrip import Strand
from lib.stubstrip import CliStrand
from lights_controller import LightsController
from monitors.jenkins_monitor import JenkinsMonitor
from pollers.jenkins_poller import JenkinsPoller

logging.basicConfig(
    level=logging.INFO,
    filename="{0}/logs/pipeline.log".format(os.environ['RPI_HOME']),
    format="%(asctime)s <%(threadName)s>: %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger()

def main():

    # TODO config
    jobs = ['Truman', 'ChannelApi', 'Security-POC']
    strand = CliStrand() # default to cli strand

    # check to see if we're not running in cli mode
    if  (len(sys.argv) == 1) or (sys.argv[1] != 'cli'):
        strand = Strand()

    lights_controller = LightsController(jobs, strand)
    lights_controller.random()

    # test!!
    build_monitor = JenkinsMonitor(jobs, lights_controller)
    sleep(3.0)
    build_monitor.process_build(dict(jobs=[dict(name='Truman', color='blue_anime')]))
    sleep(3.0)
    build_monitor.process_build(dict(jobs=[dict(name='Truman', color='blue')]))
    sleep(3.0)
    build_monitor.process_build(dict(jobs=[dict(name='Truman', color='blue_anime')]))
    sleep(3.0)
    build_monitor.process_build(dict(jobs=[dict(name='Truman', color='red')]))
    sleep(1.0)
    # end test!!

    # while True:
    #     try:
    #         # start polling jenkins
    #         build_monitor = JenkinsMonitor(jobs, lights_controller)
    #         JenkinsPoller(build_monitor).start()
    #     except KeyboardInterrupt:
    #         log.info('^C received, shutting down controller')
    #         lights_controller.off()
    #         sys.exit()
    #     except:
    #         log.error( "Unexpected error: %s", sys.exc_info()[0] )
    #         log.error( traceback.format_exc() )

    #         # log.error( "exc_info: %s", sys.exc_info() )
    #         lights_controller.error()

if __name__ == '__main__':
    main()
