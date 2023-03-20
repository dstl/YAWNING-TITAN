# run yawning titan gui from command line

### Set up dependencies
NPM can be used as the default package manager, but yarn is recommended:
- `npm install -g yarn`
- navigate to the root of the network editor project
- `yarn install`

### Building the network editor files
- navigate to the root of the network editor project (`<YAWNING_TITAN_ROOT_DIRECTORY>/yawning_titan_gui/network_editor/`)
- `yarn build`

#### Run the django server:
- navigate to repository root
- run `python ./manage.py runserver`

#### Run the django server in a minified chrome window:
- navigate to repository root
- run `python ./manage.py`
