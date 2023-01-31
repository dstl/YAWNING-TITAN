
const fs = require('fs');

/**
  * File used to parse the output of license report and
  * convert it into a sphinx compatible CSV so it can be
  * seen on the docs page
*/

let report = fs.readFileSync('license-report.csv', { encoding: 'utf-8' }).split(/\r?\n/).slice(2).filter(line => line != '');

// output to file
fs.writeFileSync('../../docs/source/network-editor-dependencies.csv', `${'Name,Version,License,URL'+'\n'}${report.join('\n')}`)
