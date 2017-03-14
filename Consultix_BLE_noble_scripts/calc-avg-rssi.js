var fs = require("fs");


var data = fs.readFileSync('test-mean.txt').toString();

function mean_rssi_of(beacon_name){
console.log("\ncalculating "+beacon_name+" mean ..");
var part = data;
var rssi = "";
var rssi_sum = 0;
var mean_rssi = 0;
var n = 0;
	while (part.indexOf(beacon_name) != -1){
		n++;
		console.log("reading "+n);
		rssi = part.substr((part.indexOf(beacon_name)+beacon_name.length+7),3);
		rssi_sum = rssi_sum + parseInt(rssi);
		mean_rssi = rssi_sum/n;
		part = part.substring(part.indexOf(beacon_name)+beacon_name.length+7);
	}
return mean_rssi;
}


console.log('estimote mean rssi is ' + mean_rssi_of("estimote"));
console.log('MiniBeacon_04864 mean rssi is ' + mean_rssi_of("MiniBeacon_04864"));
console.log('MiniBeacon_04867 mean rssi is ' + mean_rssi_of("MiniBeacon_04867"));
