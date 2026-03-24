
# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  SPDX-License-Identifier: GPL-3.0-or-later
# ------------------------------------------------------------------------------

import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import re
import glob
import shutil
from datetime import datetime


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

    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                        handlers=handlers,
                        level=logging.DEBUG,
                        force=True)


def appname(config_dir, file_path):
    """Extron the application name from the full path to the """


def config_files():
    """Generator that returns the configuration files of the latest version of Extron apps
    installed on the system.

    """
    for folder in ('Extron', 'Extron_Electronics'):
        extr_cfg_dir = os.path.expanduser('~\\AppData\\Local\\' + folder)

        app_config_dirs = glob.glob(extr_cfg_dir + r'\*.exe_Url*')

        for app_dir in app_config_dirs:
            # Get all config directories, each app version that ever existed on the PC has
            # its own directory named after its version.
            cfg_dirs = []
            for entry in os.scandir(app_dir):
                if entry.is_dir():
                    dir_name = entry.name
                    try:
                        # remove occasion additions to the directory name
                        vers_part = dir_name.split('-')[0]
                        vers_nrs = tuple(int(k) for k in vers_part.split('.'))
                        cfg_dirs.append({'dir_name': dir_name, 'vers': vers_nrs})
                    except (ValueError, TypeError):
                        # Is not a folder containing a configuration file
                        continue

            # Find the config directory of the latest app version
            cfg_dirs.sort(key=lambda x: x['vers'])
            try:
                latest_vers = cfg_dirs[-1]
            except IndexError:
                _logger.warning("Cannot find any application config directory in '%s'.", app_dir)
                continue

            # Construct the full path to the current user config file and check if it actually exists
            cfg_path = os.path.join(app_dir, latest_vers['dir_name'], 'user.config')
            if os.path.isfile(cfg_path):
                app_name = cfg_path[len(extr_cfg_dir) + 1:].split('.exe')[0]
                _logger.debug('Found user config for %s, version %s.%s.%s.%s,',
                              app_name, *latest_vers['vers'])
                yield cfg_path, app_name, latest_vers['vers']
            else:
                _logger.warning('No user config file present in folder %s.', os.path.basename(cfg_path))



def disable_whatsnew(config_file: str):
    """Write today's date in the Extron apps user config in order to prevent that annoying and
    time-consuming "What's New" web page to show up.

    :param str config_file: The full path to the config file of an Extron application.

    """

    # make a backup of the user config file
    backup_file_name = config_file + '.bak'
    shutil.copyfile(config_file, backup_file_name)

    today = datetime.today().strftime('%Y-%m-%d')
    searchpattern = br'(WhatsNewLastShown?Date\" serializeAs=\"String\">\s*<value)>\d{4}-\d{2}-\d{2}(</value>)'
    replacepattern = br'\1>' + today.encode() + br'\2'

    # Set the last show date of that "What's N&*@£$%..." to today
    with open(config_file, 'r+b') as f:
        content = f.read()
        new_content = re.sub(searchpattern, replacepattern, content, count=1)
        if content != new_content:
            with open(backup_file_name, 'wb') as backup:
                backup.write(content)
            f.seek(0)
            f.truncate()
            f.write(new_content)
            _logger.info('Changed WhatsNewLastShownDate to %s in %s', today, config_file)
        else:
            _logger.debug("What's New Date not present in File '%s', or already set to today (%s)", config_file, today)
    return True


def run():
    try:
        for app_config, _, __ in config_files():
            disable_whatsnew(app_config)
    except:
        _logger.critical("Unhandled exception:\n", exc_info=True)


if __name__ == '__main__':
    init_logging()
    _logger.critical('------ Start WhatsNewKiller ------')
    run()
    _logger.critical('------ End WhatsNewKiller ------')
