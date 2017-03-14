//to work properly this file must be copied in the /noble-modules/bleacon/estimote/ directory
var async = require('async');

var prompt = require('prompt');

var newInterval = 2000;

var Estimote = require('./estimote.js');

Estimote.discover(function(estimote) {

  async.series([
    function(callback) {
	prompt.start();
	prompt.get(['interval'], function(err,input){
	newInterval = input.interval;
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
      estimote.readAdvertisementInterval(function(error, advertisementInterval) {
        console.log('Previous advertisement interval = ' + advertisementInterval + ' ms');
	console.log('new Advertisement Interval = ' + newInterval + ' ms');
	estimote.writeAdvertisementInterval(newInterval, callback);
      });
    },
    function(callback) {
      console.log('disconnect');
      estimote.disconnect(callback);
    }
  ]);
});
