var MiniBeacon = require('minew-minibeacon');
MiniBeacon.discover(function(device) {
  device.connectAndSetup(function(err) {
    if (err) {
      return console.log('Failed to connect=', err.message);
    }
    console.log('Device is connected');
  });
})
