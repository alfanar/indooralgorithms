var fs = require("fs");


var data = fs.readFileSync('test-kalman-accuracy.txt').toString();

var n = 0;
var x_n_until_mean = 0;
var y_n_until_mean = 0;

var KG = 0;

function kalman_accuracy(){
console.log("\ncalculating kalman accuracy ..");
var part = data;
var mes_err = 0.5;
var est_err = 0.2;
var x_mes = 0;
var x_est = 0.2;
var y_mes = 0;
var y_est = 0.2;

var x_mean = 0.34;
var y_mean = 0.24;
	while (part.indexOf('.') != -1){
		KG = est_err/(est_err+mes_err);
		n++;
		console.log("reading "+n);
		x_mes = parseInt(part.substring(part.indexOf('.')-1,part.indexOf(',')-1));
		x_est = x_est + KG*(x_mes - x_est);
		if(x_est > x_mean){
			x_n_until_mean++;
		}
		part = part.substring(part.indexOf(','));
		y_mes = parseInt(part.substring((part.indexOf('.')-1),part.indexOf('\n')-1));
		y_est = y_est + KG*(y_mes - y_est);
		part = part.substring(part.indexOf('\n'));
		est_err = (1 - KG)*est_err;
		if(y_est > y_mean){
			y_n_until_mean++;
		}
	}
var acc_est = [x_est,y_est];
return acc_est;
}

var accuracy = kalman_accuracy();
console.log('\nx accuracy = '+accuracy[0]+'\ny accuracy = '+accuracy[1]);
console.log('\nno of samples is '+n);
console.log('\nno of x samples until mean is '+x_n_until_mean);
console.log('\nno of y samples until mean is '+y_n_until_mean);
console.log('\nKalman Gain is '+KG);
