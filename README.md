# WhatsNewKiller

An increasing number of software applications produced by Extron Electronics 
open a "What's New" page in your default browser when the app starts up, 
which many users find very annoying. 

WhatsNewKiller is a small software tool designed to prevent the "What's New" 
web pages from automatically popping up. It works by updating the 
`WhatsNewLastShownDate` in the application's `user.config` files to the 
current date, before you start using these apps. As a result, these pages 
will never be displayed again. 

Whenever WhatsNewKiller changes a user config file, the file's old content 
will be written to a backup file, overwriting a possible previous backup. 
WhatsnewKiller writes all actions it takes to a log file located in 
`%USERPROFILE%\AppData\Local\Extron`.

>[!IMPORTANT] 
> As a small open source project, both the WhatsNewKiller executable and the 
> installer are not signed. They will be regarded as "unrecognized app" by 
> Windows and will trigger a warning on first use. In order to continue, 
> click on `More info` in the warning dialog and then click the button `Run
> anyway`. 

## Usage
The whole idea of WhatsNewKiller is to install and forget. After installation 
with the default options, the killer will run automatically each time you log 
on to your computer and at midnight, but it's perfectly possible to run it 
manually as well.

### GUI Mode (Default)

By default, WhatsNewKiller launches with a simple uer interface when opened 
manually.
- Click **"Run Killer"** to scan and update Extron config files.
- The log window will display the actions taken and any applications found.

### CLI / Background Mode

Open a command prompt in the folder containing the executable and type:

```bash
whatsnewkiller.exe nogui
```

This mode is ideal for scheduled tasks or startup scripts.


## Installation

### Installer

Download the latest version of WhatsNewKiller_xxx_setup.exe from 
[GitHub releases](https://github.com/dimkroon/whatsnewkiller/releases)
Run the installer and follow the directions on the screen. The installer runs 
without admin privileges and installs WhatsNewKiller for the current user only. 

During installation, you will be presented with the following options:
- **Run WhatsNewKiller at login.**
  Select this if you want to disable WhatsNew each time you log in to your 
  computer. This is usually enough for most use cases where users turn off 
  their computer at the end of a job or day.
- **Run WhatsNewKiller at midnight.**
  This creates a task in Windows task scheduler to run WhatsNewKiller every 
  day just past midnight, to ensure What's New is disabled if you leave your
  computer running overnight.

> [!NOTE] 
> Some use cases are not covered by either of these option. e.g. If you 
> wake your computer from sleep or hibernation, no login will trigger 
> WhatsNewKiller and the scheduled event at midnight won't run when the 
> PC is in hibernation. 


### Manual installation

- Download the latest version of WhatsNewKiller.exe from 
  [GitHub releases](https://github.com/dimkroon/whatsnewkiller/releases)
- Place the file in a location of your choice, e.g. 
  `%USERPROFILE%\AppData\Local\Programs\WhatsNewKiller`.
- Open Windows taskscheduler and create a task to run WhatsNewKiller at user 
  logon, and/or any other trigger that works for you. 
- Ensure to append argument `nogui` when you define the action.


### Running from Source

1.  **Clone the repository:**
    ```cmd
    git clone https://github.com/dimkroon/whatsnewkiller.git
    cd whatsnewkiller
    ```
    
2. **Run the application:**
   - with gui:
       ```cmd
       python src/whatsnewkiller.py
       ```
   - without gui:
       ```cmd
       python src/whatsnewkiller.py nogui
       ```

## Issues
The current version is solely based on my own experience with software from 
Extron on my own computers. If you find a bug, have a problem, questing, or 
things just don't seem to work for you as well as could be expected, please 
open an issue here at GitHub and provide a clear and detailed description of 
the problem.

## Build

Although the sript runs on any recent version of Python-3 without the need 
to build, a windows executable and installer can be created to support users 
who don't have Python installed, or prefer a simple way to install and configure 
the program.

### Build a Windows executable
This requires pyinstaller to be installed in your Python environment.

Download the source code, open a command prompt and navigate to the base 
directory containing the source. Ensure you have python installed.

To create a standalone `.exe` using PyInstaller:

```bash
pyinstaller --onefile --noconsole --icon=src/wnk.ico --add-data=src/wnk.ico:. --version-file src/version.txt src/whatsnewkiller.py
```

The resulting executable will be in the `dist/` directory.

### Building the Installer

The project uses Inno Setup 6 to create a Windows installer.

1.  Build the executable first (see above).
2.  Open `setup.iss` in Inno Setup Compiler and compile it.
3.  The installer will be generated in the `Output/` directory.

## Contributing
Contributions are most welcome. This is a small project with few or no rules.
Please use common sense and decency and format your code in accordance with 
PEP8. As this program is meant to run at computer start up, the intention is to 
keep everything small with limited impact on start up time. 

For bug fixes and small improvements, just open a PR against the main branch.
If you wish to propose more significant changes, it's probably best to 
create an issue first to discuss them.

## License

This project is licensed under the **GNU GPL v3.0 or later**. See 
[LICENSE.md](LICENSE.md) and [COPYRIGHT.txt](COPYRIGHT.txt) for details.

Copyright (c) 2026 Dimitri Kroon.
