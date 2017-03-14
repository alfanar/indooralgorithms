// Scanning for iBeacons in General

var Bleacon = require('bleacon');
Bleacon.on('discover', function(bleacon) {
  console.log('bleacon found: ' + JSON.stringify(bleacon));
});

Bleacon.startScanning();

