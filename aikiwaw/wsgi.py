activate_this = 'home/pawkow/envs/aikiblog/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import os
import sys

path = '/home/pawkow/aikiblog/'
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'aikiwaw.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()