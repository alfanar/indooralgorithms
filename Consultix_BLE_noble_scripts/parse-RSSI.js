var noble = require('./index');


noble.on('stateChange', function(state) {

  if (state === 'poweredOn') {
    noble.startScanning();
  } else {
    noble.stopScanning();
  }
});

noble.on('discover', function(peripheral) {
var per = peripheral.toString();
var mac = per.substring( 31 , 50 );
var name = '';

if ( per.substr(per.indexOf('\"localName\"\:')+13,1) == 'e'){
name = per.substr( per.indexOf('\"localName\"\:')+12 , 10 );
}
else if ( per.substr(per.indexOf('\"localName\"\:')+13,1) == 'M'){
name = per.substring( per.indexOf('\"localName\"\:')+12 , per.indexOf('\,\"txPowerLevel\"') );
}

var rssi = per.substr( per.indexOf('\"rssi\"\:')+7 , 3 );

  console.log('MAC ' + mac);
  console.log('NAME ' + name);
  console.log('RSSI ' + rssi);
  process.exit();
});

//Peripheral =

/*
{"id":"d05fb83af579",           --21--
"address":"d0:5f:b8:3a:f5:79",  --51--
"addressType":"public",         --74--
"connectable":true,             --93--
"advertisement":{               --110--
"localName":"MiniBeacon_04867", --141--
"txPowerLevel":0,
"manufacturerData":{
"type":"Buffer",
"data":[76,0,2,21,226,197,109,181,223,251,72,210,176,96,208,245,167,16,150,224,0,0,0,0,197]},
"serviceData":[],
"serviceUuids":[],
"solicitationServiceUuids":[],
"serviceSolicitationUuids":[]},
"rssi":-49,
"state":"disconnected"}
*/
