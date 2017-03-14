var fs = require("fs");


var data = fs.readFileSync('test-mean.txt').toString();

function rssi_variance_of(beacon_name,mean,no_of_samples){
console.log("\ncalculating "+beacon_name+" variance ..");
var part = data;
var rssi = "";
var variance = 0;
	while (part.indexOf(beacon_name) != -1){
		rssi = part.substr((part.indexOf(beacon_name)+beacon_name.length+7),3);
		variance = variance + (Math.pow(mean - parseInt(rssi),2)/no_of_samples);
		part = part.substring(part.indexOf(beacon_name)+beacon_name.length+7);
	}
return variance;
}


console.log('estimote rssi variance is ' + rssi_variance_of("estimote",-68.64119134588367,3559));
console.log('estimote rssi std dev is ' + Math.sqrt(rssi_variance_of("estimote",-68.64119134588367,3559)));
console.log('MiniBeacon_04864 rssi variance is ' + rssi_variance_of("MiniBeacon_04864",-67.07631498935847,3289));
console.log('MiniBeacon_04864 rssi std dev is ' + Math.sqrt(rssi_variance_of("MiniBeacon_04864",-67.07631498935847,3289)));
console.log('MiniBeacon_04867 rssi variance is ' + rssi_variance_of("MiniBeacon_04867",-76.78489847715736,3152));
console.log('MiniBeacon_04867 rssi std dev is ' + Math.sqrt(rssi_variance_of("MiniBeacon_04867",-76.78489847715736,3152)));
