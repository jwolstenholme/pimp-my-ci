
import Queue
from threading import Thread
from time import sleep
from lib.build_job import BuildJob
from monitors.jenkins_monitor import JenkinsMonitor
from monitors.travis_monitor import TravisMonitor
from pollers.http_json_poller import HttpJsonPoller
from pollers.travis_poller import TravisPoller

def worker(controllers, job, queue):
  while True:
    try:
        status = queue.get_nowait()
        for controller in controllers:
            controller.update_build_status(job, status)
        queue.task_done()
    except Queue.Empty:
        sleep(1)

# to represent a collection of build jobs
class BuildJobs(list):

    def __init__(self, defaults, job_dictionaries):
        # set up jobs
        for job_description in job_dictionaries:
            self.append( BuildJob(dict(defaults.items() + job_description.items())) )

        # create queues & names to be used later
        self.queues = dict([ (job.name, job.queue) for job in self ])
        self.names = [ job.name for job in self ]

    def create_threads(self, controllers):
        for job in self:
            t = Thread(target=worker, args=(controllers, job, job.queue, ))
            t.daemon = True
            t.start()

    @staticmethod
    def from_dictionaries(platform, defaults, job_dictionaries):
        if platform == 'jenkins':
            return JenkinsBuildJobs(defaults, job_dictionaries)
        elif platform == 'travis':
            return TravisBuildJobs(defaults, job_dictionaries)
        else:
            raise ValueError('platform must be one of [jenkins, travis]')


class JenkinsBuildJobs(BuildJobs):

    def __init__(self, defaults, job_dictionaries):
        BuildJobs.__init__(self, defaults, job_dictionaries)
        self.url = defaults['url']

    def start_polling(self, controllers):
        self.create_threads(controllers)
        monitor = JenkinsMonitor(self.queues)
        HttpJsonPoller(self.url, monitor).start()

class TravisBuildJobs(BuildJobs):

    def start_polling(self, controllers):
        self.create_threads(controllers)
        monitor = TravisMonitor(self.queues)
        TravisPoller(self, monitor).start()

