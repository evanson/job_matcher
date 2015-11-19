import sys
import os

from twisted.application import internet, service
from twisted.web import server, resource, wsgi, static
from twisted.internet import reactor
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver, FileLogObserver


PORT = 9090
HOME = '/app/job_matcher'
LOGDIR = '/app/log/job_matcher'
LOG = 'job_matcher.log'

sys.path.append(HOME)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_matcher.settings")

from job_matcher.wsgi import application as djapp

application = service.Application('job_matcher')
root = wsgi.WSGIResource(reactor, reactor.getThreadPool(), djapp)
logfile = DailyLogFile(LOG, LOGDIR)

application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

main_site = server.Site(root)
internet.TCPServer(PORT, main_site).setServiceParent(application)
reactor.suggestThreadPoolSize(100)
