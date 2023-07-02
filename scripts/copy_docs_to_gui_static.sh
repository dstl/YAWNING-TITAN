# Create directory if it doesn't exist
if [ ! -d "../src/yawning_titan_gui/static/docs" ]; then
    mkdir "../src/yawning_titan_gui/static/docs"
fi

# Delete all files in the directory
rm -rf ../src/yawning_titan_gui/static/docs/*

# Copy all files from the source directory to the destination directory
cp -r ../docs/_build/html/* ../src/yawning_titan_gui/static/docs/
