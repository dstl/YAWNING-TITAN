=====================
Creating an installer
=====================

To create a .spec file to use with pyinstaller run the command:

pyinstaller manage.py

If the .spec file is being built from scratch it is good practice to add a .ico file to the exe arguments as well as amending all references to name to match the Yawning-Titan project name. also switching off console prevents a console window from opening when the yawning_titan.exe file is ran.

exe = EXE(
  ...,
  icon='path/to/icon.ico',
  name='Yawning-Titan',
  console=False,
)


If the .spec file is built from scratch we must also be sure to point the hidden 'flaskwebgui' package in the hidden imports section.

To build the distributable files using pyinstaller run the command

pyinstaller manage.spec

To create a windows installer using InstallForge

Creating an installer

To create our installer we'll be using a tool called InstallForge. InstallForge is free and you can download the installer from this page.

General

run InstallForge  an open the general tab. Enter the basic information for the yawning_titan instance.

You can also select the target platforms for the installer, from various versions of Windows that are available. For desktop applications you currently probably only want to target Windows 7, 8 and 10.

Setup

Click on the left sidebar to open the "Files" page under "Setup". Here you can specify the files to be bundled in the installer.

Use "Add Files…" and select all the files in the dist/yawning_titan folder produced by PyInstaller. The file browser that pops up allows multiple file selections, so you can add them all in a single go, however you need to add folders separately. Click "Add Folder…" and add any folders under dist/yawning_titan

Once you're finished scroll through the list to the bottom and ensure that the folders are listed to be included. You want all files and folders under dist/yawning_titan to be present. But the folder dist/yawning_titan itself should not be listed.

Navigate to the "Uninstall" tab, and attach an unistaller by ticking the box. This will also make the application appear in "Add or Remove Programs".

System

Under "System" select "Shortcuts" to open the shortcut editor. Here you can specify shortcuts for both the Start Menu and Desktop if you like.

Click "Add…" to add new shortcuts for your application. Choose between Start menu and Desktop shortcuts, and fill in the name and target file. This is the path your application EXE will end up at once installed. Since <installpath>\ is already specified, now add the name yawning_titan to the app exe.

Build

With the basic settings in place, you can now build your installer.

At this point you can save your InstallForge project so you can re-build the installer from the same settings in future.

Click on the "Build" section at the bottom to open the build panel.

Click on the large icon button to start the build process. If you haven't already specified a setup file location you will be prompted for one. This is the location where you want the completed installer to be saved.

The build process will began, collecting and compressing the files into the installer.

Running the installer

The installer itself shouldn't have any surprises, working as expected. Depending on the options selected in InstallForge you may have extra panels or options.

Step through the installer until it is complete. You can optionally run the application from the last page of the installer, or you can find it in your start menu.
