var fs = require("fs");

var measuredPower_1 = -68.64119134588367;
var measuredPower_2 = -67.07631498935847;
var measuredPower_3 = -76.78489847715736;
var data = fs.readFileSync('out.txt').toString();
var beacons_pos_data = fs.readFileSync('pos.txt').toString();

function square(x){
	return Math.pow(x,2);
}

function cramer_pos_2D(x1,y1,x2,y2,x3,y3,d1,d2,d3){
	var x = ( 2*(y3-y1)*((square(d1)-square(d2))-(square(x1)-square(x2))-(square(y1)-square(y2))) - 2*(y2-y1)*((square(d1)-square(d3))-(square(x1)-square(x3))-(square(y1)-square(y3))) )/(4*(x2-x1)*(y3-y1)-4*(x3-x1)*(y2-y1));
	var y = ( 2*(x2-x1)*((square(d1)-square(d3))-(square(x1)-square(x3))-(square(y1)-square(y3))) - 2*(x3-x1)*((square(d1)-square(d2))-(square(x1)-square(x2))-(square(y1)-square(y2))) )/(4*(x2-x1)*(y3-y1)-4*(x3-x1)*(y2-y1));

	var pos = [x,y];
	return pos;
}

function beacons_pos(pos_data){
	var x1 = parseFloat(pos_data.substring(pos_data.indexOf('x1=')+3,pos_data.indexOf('y1=')));
	var y1 = parseFloat(pos_data.substring(pos_data.indexOf('y1=')+3,pos_data.indexOf('x2=')));
	var x2 = parseFloat(pos_data.substring(pos_data.indexOf('x2=')+3,pos_data.indexOf('y2=')));
	var y2 = parseFloat(pos_data.substring(pos_data.indexOf('y2=')+3,pos_data.indexOf('x3=')));
	var x3 = parseFloat(pos_data.substring(pos_data.indexOf('x3=')+3,pos_data.indexOf('y3=')));
	var y3 = parseFloat(pos_data.substring(pos_data.indexOf('y3=')+3));

//	console.log('node_1 position is ('+x1+','+y1+')');
//	console.log('node_2 position is ('+x2+','+y2+')');
//	console.log('node_3 position is ('+x3+','+y3+')');

	var beacons_pos = [x1,y1,x2,y2,x3,y3];
	return beacons_pos;
}

//console.log('data is\n'+data);

if(data.indexOf('estimote') != -1){

//console.log('estimote is there');

	if(data.indexOf('MiniBeacon_04864') != -1){

//	console.log('MiniBeacon_04864 is there');

		if(data.indexOf('MiniBeacon_04867') != -1){

//			console.log('MiniBeacon_04867 is there');
			var rssi_1 = parseInt(data.substr((data.substring(0,data.indexOf('estimote')).lastIndexOf('rssi')+6),3));
			var rssi_2 = parseInt(data.substr((data.substring(0,data.indexOf('MiniBeacon_04864')).lastIndexOf('rssi')+6),3));
			var rssi_3 = parseInt(data.substr((data.substring(0,data.indexOf('MiniBeacon_04867')).lastIndexOf('rssi')+6),3));
//			console.log('rssi_1 = '+data.substr((data.substring(0,data.indexOf('estimote')).lastIndexOf('rssi')+6),3)+' w/ value of '+rssi_1);
//			console.log('rssi_2 = '+data.substr((data.substring(0,data.indexOf('MiniBeacon_04864')).lastIndexOf('rssi')+6),3)+' w/ value of '+rssi_2);
//			console.log('rssi_3 = '+data.substr((data.substring(0,data.indexOf('MiniBeacon_04867')).lastIndexOf('rssi')+6),3)+' w/ value of '+rssi_3);
			var accuracy_1 = Math.pow(12.0, 1.5 * ((rssi_1 / measuredPower_1) - 1));
			var accuracy_2 = Math.pow(12.0, 1.5 * ((rssi_2 / measuredPower_2) - 1));
			var accuracy_3 = Math.pow(12.0, 1.5 * ((rssi_3 / measuredPower_3) - 1));
//			console.log('accuracy_1 = '+accuracy_1);
//			console.log('accuracy_2 = '+accuracy_2);
//			console.log('accuracy_3 = '+accuracy_3);
			var b_pos = beacons_pos(beacons_pos_data);
			var pos = cramer_pos_2D(b_pos[0],b_pos[1],b_pos[2],b_pos[3],b_pos[4],b_pos[5],accuracy_1,accuracy_2,accuracy_3);
			console.log('RPi3 position is ('+pos[0]+','+pos[1]+')');
			if((pos[0] != NaN) & (pos[1] != NaN)){
				fs.appendFileSync('test-accuracy.txt','\n'+pos+'\n');
			}
      
		}else{
		console.log('MiniBeacon_04867 is missing');
		}
	}else{
	console.log('MiniBeacon_04864 is missing');
	}
}else{
console.log('estimote is missing');
}
/*
						-----------------
						-- data sample --
						-----------------

scanning instance ---------------------'Mon Nov  7 12:37:34 UTC 2016'------------------------
bleacon found: {"uuid":"e2c56db5dffb48d2b060d0f5a71096e0","major":0,"minor":0,"measuredPower":-59,"rssi":-71,"accuracy":2.134232534620913,"proximity":"near","localname":"MiniBeacon_04864"}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-54,"accuracy":0.6181960281591174,"proximity":"near","localname":"f95d89a\""}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-82,"accuracy":3.328008860553303,"proximity":"near","localname":"f95d89a\""}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-70,"accuracy":1.617609875265343,"proximity":"near","localname":"f95d89a\""}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-74,"accuracy":2.0573618592724032,"proximity":"near","localname":"f95d89a\""}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-52,"accuracy":0.5481605323489872,"proximity":"near","localname":"f95d89a\""}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-69,"accuracy":1.5232267778301263,"proximity":"near","localname":"f95d89a\""}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-52,"accuracy":0.5481605323489872,"proximity":"near","localname":"f95d89a\""}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-52,"accuracy":0.5481605323489872,"proximity":"near","localname":"f95d89a\""}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-83,"accuracy":3.5342209552476445,"proximity":"near","localname":"f95d89a\""}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-83,"accuracy":3.5342209552476445,"proximity":"near","localname":"estimote"}
bleacon found: {"uuid":"e2c56db5dffb48d2b060d0f5a71096e0","major":0,"minor":0,"measuredPower":-59,"rssi":-60,"accuracy":1.0652138666865865,"proximity":"near","localname":"83af579\""}
bleacon found: {"uuid":"e2c56db5dffb48d2b060d0f5a71096e0","major":0,"minor":0,"measuredPower":-59,"rssi":-62,"accuracy":1.2086774899735395,"proximity":"near","localname":"MiniBeacon_04867"}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-70,"accuracy":1.617609875265343,"proximity":"near","localname":"estimote"}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-69,"accuracy":1.5232267778301263,"proximity":"near","localname":"estimote"}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-85,"accuracy":3.985769182995162,"proximity":"near","localname":"estimote"}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-69,"accuracy":1.5232267778301263,"proximity":"near","localname":"estimote"}
bleacon found: {"uuid":"e2c56db5dffb48d2b060d0f5a71096e0","major":0,"minor":0,"measuredPower":-59,"rssi":-62,"accuracy":1.2086774899735395,"proximity":"near","localname":"MiniBeacon_04867"}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-69,"accuracy":1.5232267778301263,"proximity":"near","localname":"estimote"}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-69,"accuracy":1.5232267778301263,"proximity":"near","localname":"estimote"}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-69,"accuracy":1.5232267778301263,"proximity":"near","localname":"estimote"}
bleacon found: {"uuid":"e2c56db5dffb48d2b060d0f5a71096e0","major":0,"minor":0,"measuredPower":-59,"rssi":-65,"accuracy":1.4609012747687342,"proximity":"near","localname":"MiniBeacon_04864"}
bleacon found: {"uuid":"b9407f30f5f8466eaff925556b57fe6d","major":22349,"minor":3,"measuredPower":-62,"rssi":-70,"accuracy":1.617609875265343,"proximity":"near","localname":"estimote"}
bleacon found: {"uuid":"e2c56db5dffb48d2b060d0f5a71096e0","major":0,"minor":0,"measuredPower":-59,"rssi":-73,"accuracy":2.421672214040427,"proximity":"near","localname":"MiniBeacon_04867"}
*/
