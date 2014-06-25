# script expects RPI_HOME to be set as an env var

import sys
import os
import logging
import traceback
import Queue

from time import sleep
from lib.ledstrip import Strand
from lib.stubstrip import CliStrand
from lib.build_job import BuildJob
from lib.lights_controller import LightsController
from monitors.jenkins_monitor import JenkinsMonitor
from pollers.jenkins_poller import JenkinsPoller

print 'RPI_HOME: ', os.environ['RPI_HOME']

logging.basicConfig(
    level=logging.INFO,
    filename="{0}/logs/pipeline.log".format(os.environ['RPI_HOME']),
    format="%(asctime)s <%(threadName)s>: %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p',
    maxBytes=1024,
    backupCount=3)
log = logging.getLogger()

def main():
    # TODO config
    num_leds = 5
    build_jobs = [
        BuildJob(name='Monitor U 01 Channel Arrangement', num_leds=num_leds),
        BuildJob(name='Truman-ios',                       num_leds=num_leds),
        BuildJob(name='MonkeyTalk',                       num_leds=num_leds),
        BuildJob(name='Android_Commit',                   num_leds=2, offset=0),
        BuildJob(name='Android_Functional',               num_leds=2, offset=0),
        BuildJob(name='Android_Hockey_Deploy',            num_leds=1),
        BuildJob(name='ChannelApi',                       num_leds=num_leds)
    ]

    job_queues = {job.name: Queue.Queue() for job in build_jobs}

    strand = CliStrand()  # default to cli strand

    # check to see if we're not running in cli mode
    if (len(sys.argv) == 1) or (sys.argv[1] != 'cli'):
        strand = Strand()

    lights_controller = LightsController(strand, job_queues, build_jobs)
    lights_controller.off()

    # start polling jenkins
    build_monitor = JenkinsMonitor(job_queues)
    JenkinsPoller(build_monitor).start()

    while True:
        try:
            sleep(0.05)
        except KeyboardInterrupt:
            log.info('^C received, shutting down controller')
            lights_controller.off()
            sys.exit()
        except:
            log.error("Unexpected error: %s", sys.exc_info()[0])
            log.error(traceback.format_exc())

            # log.error( "exc_info: %s", sys.exc_info() )
            lights_controller.error()

if __name__ == '__main__':
    main()
