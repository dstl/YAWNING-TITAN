# NodeEditor

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 15.0.3.

## Prerequisites
- An installation of Node 18 or above

This can be done via NVM
- Install [NVM](https://github.com/coreybutler/nvm-windows)
- On an admin terminal run: `nvm install 18.12.1`

Or can be installed from [NodeJS.org](https://nodejs.org/en/download/)

### Set up dependencies
NPM can be used as the default package manager, but yarn is recommended:
- `npm install -g yarn`
- navigate to the root of the network editor project
- `yarn install`

### Run the node editor:
- navigate to the root of the network editor project
- `yarn start`
- open http://localhost:4200/ in browser

### Run node editor unit tests
- navigate to the root of the network editor project
- `yarn test`

### Run node editor end to end tests
If the node editor has not been built yet, follow the "Building the node editor files" step.

#### Run the django server:
- navigate to repository root
- run `python ./manage.py runserver`

#### Run the end to end test via GUI:
- navigate to the root of the network editor project
- `yarn test:e2e`
- Select "E2E Testing"
- YT GUI was developed primary for Chrome, however,
should work in other browsers - select any browser
then press "Start E2E Testing"
- In the new window that opens, select any test to run

#### Run the end to end test:
- navigate to the root of the network editor project
- `yarn test:e2e:ci`

### Building the node editor files
- navigate to the root of the network editor project
- `yarn build`

### Updating the Network Editor dependencies
Every time a new package is added or `yarn install` (or `yarn`) is run, the post install script will be run.

This should automatically update the network-editor-dependencies.csv which is used by Sphinx to build the docs.
To update the docs locally, rebuild the docs:
- navigate to the docs directory (YAWNING-TITAN/docs)

Windows: `.\make.bat html`

Linux: `make html`

### Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.
