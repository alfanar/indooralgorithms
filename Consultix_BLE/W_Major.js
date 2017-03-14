//to work properly this file must be copied in the /noble-modules/bleacon/estimote/ directory
var async = require('async');

var prompt = require('prompt');

var newMajor = 22349;

var Estimote = require('./estimote.js');

Estimote.discover(function(estimote) {

  async.series([
    function(callback) {
	prompt.start();
	prompt.get(['Major'], function(err,input){
	newMajor = input.Major;
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
      estimote.readMajor(function(error, major) {
        console.log('Previous Major = ' + major + ' (0x' + major.toString(16) + ')');
        console.log('new Major = ' + newMajor);
        estimote.writeMajor(newMajor, callback);
      });
    },
    function(callback) {
      console.log('disconnect');
      estimote.disconnect(callback);
    }
  ]);
});
