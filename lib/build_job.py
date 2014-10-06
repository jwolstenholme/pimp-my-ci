
import Queue

from threading import Thread
from time import sleep
from lib.config import Config
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

# TODO rename all these to just 'job'
class BuildJob:

    def __init__(self, dictionary):
        self.name       = dictionary.get('name')
        self.url        = dictionary.get('url')
        self.num_leds   = dictionary.get('num_leds', 1)
        self.offset     = dictionary.get('offset', 1)
        self.success    = dictionary.get('success', '__RANDOM')
        self.failure    = dictionary.get('failure', '__RANDOM')
        self.queue      = Queue.Queue()

        if self.is_blank(self.name):
            raise ValueError('Name must not be blank')

        if self.is_blank(self.url):
            raise ValueError('URL must not be blank')

        if self.num_leds <= 0 or self.num_leds >= Config.total_number_leds:
            raise ValueError('Invalid num_leds')

        if self.offset < 0 or self.offset >= Config.total_number_leds:
            raise ValueError('Invalid offset')

    def start_polling(self):
        print "starting polling..."
        if (self.platform == 'jenkins'):
            monitor = JenkinsMonitor(self)
            HttpJsonPoller(self, monitor).start()
            print "jenkins polling started for job", self.name
        elif (self.platform == 'travis'):
            monitor = TravisMonitor(self)
            TravisPoller(self, monitor).start()
            print "travis polling started for job", self.name

    #Returns the array of led indecies this job will occupy at the given index
    def led_addresses(self, index):
        return range(index, min(index + self.num_leds, Config.total_number_leds))

    def led_coordinates(self, index):
        addresses = self.led_addresses(index)
        return [addresses[0], (addresses[-1] + 1)]

    def next_index(self, index):
        if index >= Config.total_number_leds - 1:
            raise ArithmeticError('No leds available')
        return self.num_leds + self.offset + index

    def is_blank(self, string):
        return string is None or string.strip() == ''

    @staticmethod
    def from_dictionaries(platform, defaults, job_dictionaries):
        if platform == 'jenkins':
            return JenkinsBuildJobs(defaults, job_dictionaries)
        elif platform == 'travis':
            return TravisBuildJobs(defaults, job_dictionaries)
        else:
            raise ValueError('platform must be one of [jenkins, travis]')

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
