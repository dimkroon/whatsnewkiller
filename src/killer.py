
# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  SPDX-License-Identifier: GPL-3.0-or-later
# ------------------------------------------------------------------------------

import logging
import os
import re
import glob
import shutil
from datetime import datetime


_logger = logging.getLogger()


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
                _logger.info('Found user config for %s, version %s.%s.%s.%s,',
                              app_name, *latest_vers['vers'])
                yield cfg_path, app_name, latest_vers['vers']
            else:
                _logger.warning('No config files present in folder %s.', os.path.basename(cfg_path))


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
    _logger.debug("    Analysing file '%s'",config_file)

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
            _logger.info('    Changed WhatsNewLastShownDate to %s', today)
        else:
            if b'WhatsNewLast' in content:
                _logger.info("    What's New Date was already set to today (%s)", today)
            else:
                _logger.info("    No What's New Date.")
    return True


def run():
    _logger.critical('------ Start WhatsNewKiller ------')

    try:
        app_count = 0
        for app_config, _, __ in config_files():
            app_count += 1
            disable_whatsnew(app_config)
        if not app_count:
            _logger.info("No Extron applications found.")
    except Exception:
        _logger.critical("Unhandled exception:\n", exc_info=True)

    _logger.critical('------ End WhatsNewKiller ------')


if __name__ == '__main__':
    run()