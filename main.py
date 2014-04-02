# script expects RPI_HOME to be set as an env var

import sys
import os
import logging
import traceback
import Queue

from time import sleep
from lib.ledstrip import Strand
from lib.stubstrip import CliStrand
from lib.lights_controller import LightsController
from monitors.jenkins_monitor import JenkinsMonitor
from pollers.jenkins_poller import JenkinsPoller

print 'RPI_HOME: ', os.environ['RPI_HOME']

logging.basicConfig(
    level=logging.INFO,
    filename="{0}/logs/pipeline.log".format(os.environ['RPI_HOME']),
    format="%(asctime)s <%(threadName)s>: %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger()

def main():

    # TODO config
    jobs = ['Truman', 'ChannelApi', 'Security-POC']
    job_queues = dict.fromkeys(jobs, Queue.Queue())
    print 'job_queues: ', job_queues

    strand = CliStrand() # default to cli strand

    # check to see if we're not running in cli mode
    if  (len(sys.argv) == 1) or (sys.argv[1] != 'cli'):
        strand = Strand()

    lights_controller = LightsController(job_queues, strand)
    lights_controller.random()
    strand.update()

    # start polling jenkins
    build_monitor = JenkinsMonitor(job_queues)
    JenkinsPoller(build_monitor).start()

    while True:
        try:
#            strand.update()
            sleep(0.05)
        except KeyboardInterrupt:
            log.info('^C received, shutting down controller')
            lights_controller.off()
            sys.exit()
        except:
            log.error( "Unexpected error: %s", sys.exc_info()[0] )
            log.error( traceback.format_exc() )

            # log.error( "exc_info: %s", sys.exc_info() )
            lights_controller.error()
            strand.update()

if __name__ == '__main__':
    main()
