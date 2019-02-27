#!/usr/bin/env python

import os
from flask_script import Manager
from flask_script import Server

from app.setup import create_app

application = create_app()

if __name__ == '__main__':
    manager = Manager(application)
    port = int(os.getenv('PORT', 5000))
    manager.add_command("runserver", Server(threaded=True, host='0.0.0.0', port=port))
    manager.run()
