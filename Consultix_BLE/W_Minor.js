//to work properly this file must be copied in the /noble-modules/bleacon/estimote/ directory
var async = require('async');

var prompt = require('prompt');

var newMinor = 3;

var Estimote = require('./estimote.js');

Estimote.discover(function(estimote) {

  async.series([
    function(callback) {
	prompt.start();
	prompt.get(['Minor'], function(err,input){
	newMinor = input.Minor;
	callback();
  });
    },  
    function(callback) {
      estimote.on('disconnect', function() {
        console.log('disconnected!');
        process.exit(0);
      });

      estimote.on('motionStateChange', function(isMoving) {
        console.log('\tmotion state change: isMoving = ' + isMoving);
      });

      console.log('found: ' + estimote.toString());

      console.log('connectAndSetUp');
      estimote.connectAndSetUp(callback);
    },
    function(callback) {
      console.log('pair');
      estimote.pair(callback);
    },
    function(callback) {
      estimote.readMinor(function(error, minor) {
        console.log('Previous Minor = ' + minor + ' (0x' + minor.toString(16) + ')');
        console.log('new Minor = ' + newMinor);
        estimote.writeMinor(newMinor, callback);
      });
    },
    function(callback) {
      console.log('disconnect');
      estimote.disconnect(callback);
    }
  ]);
});
