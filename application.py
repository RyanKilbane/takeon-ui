#!/usr/bin/env python

import os
from flask_script import Manager, Server

from app.setup import create_app

application = create_app()

if __name__ == '__main__':
    manager = Manager(application)
    port = int(os.getenv('PORT', 8090))
    host = str(os.getenv('HOST', '127.0.0.1'))
    manager.add_command("runserver", Server(threaded=True, host=host, port=port))
    manager.run()
