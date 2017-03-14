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
			var rssi_1 = parseInt(data.substr(data.indexOf('estimote')+15,3));
			var rssi_2 = parseInt(data.substr(data.indexOf('MiniBeacon_04864')+23,3));
			var rssi_3 = parseInt(data.substr(data.indexOf('MiniBeacon_04867')+23,3));
//			console.log('rssi_1 = '+data.substr(data.indexOf('estimote')+15,3)+' w/ value of '+rssi_1);
//			console.log('rssi_2 = '+data.substr(data.indexOf('MiniBeacon_04864')+23,3)+' w/ value of '+rssi_2);
//			console.log('rssi_3 = '+data.substr(data.indexOf('MiniBeacon_04867')+23,3)+' w/ value of '+rssi_3);
			var accuracy_1 = Math.pow(12.0, 1.5 * ((rssi_1 / measuredPower_1) - 1));
			var accuracy_2 = Math.pow(12.0, 1.5 * ((rssi_2 / measuredPower_2) - 1));
			var accuracy_3 = Math.pow(12.0, 1.5 * ((rssi_3 / measuredPower_3) - 1));
//			console.log('accuracy_1 = '+accuracy_1);
//			console.log('accuracy_2 = '+accuracy_2);
//			console.log('accuracy_3 = '+accuracy_3);
			var b_pos = beacons_pos(beacons_pos_data);
			var pos = cramer_pos_2D(b_pos[0],b_pos[1],b_pos[2],b_pos[3],b_pos[4],b_pos[5],accuracy_1,accuracy_2,accuracy_3);
//			console.log('RPi3 position is ('+pos[0]+','+pos[1]+')');
			fs.appendFileSync('test-accuracy.txt','\n'+pos+'\n');
      
		}else{
		console.log('MiniBeacon_04867 is missing');
		}
	}else{
	console.log('MiniBeacon_04864 is missing');
	}
}else{
console.log('estimote is missing');
}
