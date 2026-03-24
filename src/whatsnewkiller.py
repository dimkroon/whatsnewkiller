# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  SPDX-License-Identifier: GPL-3.0-or-later
# ------------------------------------------------------------------------------

import os
import sys
import logging
from logging.handlers import RotatingFileHandler

__version__ = '1.0.0'

_logger = logging.getLogger()


def init_logging():
    log_folder = os.path.expanduser('~\\AppData\\Local\\Extron')
    os.makedirs(log_folder, exist_ok=True)

    file_handler = RotatingFileHandler(filename=os.path.join(log_folder, 'whatsnewkiller.log'),
                                       maxBytes=1000000,
                                       backupCount=2)

    is_debug = getattr(sys, 'gettrace', None) and sys.gettrace()
    if is_debug or os.environ.get('PYDEBUG', 'false').lower() == 'true':
        print('Running in debug mode; logging to stderr')
        handlers = None
    else:
        handlers = (file_handler, )

    logging.basicConfig(format='[%(asctime)s] [%(levelname)-8s] %(message)s',
                        handlers=handlers,
                        level=logging.DEBUG,
                        force=True)


def run_gui():
    import gui
    app = gui.App(__version__)
    app.mainloop()


def run_service():
    import killer
    killer.run()


if __name__ == '__main__':
    init_logging()
    _logger.info('### WhatsNewKiller %s', __version__)
    run_gui()
    run_service()
    if len(sys.argv) > 1 and sys.argv[1] == 'nogui':
        run_service()
    else:
        run_gui()