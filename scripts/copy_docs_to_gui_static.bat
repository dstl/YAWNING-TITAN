# Create directory if it doesn't exist
if not exist "..\src\yawning_titan_gui\static\docs" mkdir ..\src\yawning_titan_gui\static\docs

# Delete all files in the directory
del /s /q ..\src\yawning_titan_gui\static\docs\*

# Copy all files from the source directory to the destination directory
robocopy ..\docs\_build\html ..\src\yawning_titan_gui\static\docs /s
