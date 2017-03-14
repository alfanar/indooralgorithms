var fs = require("fs");


var data = fs.readFileSync('test-accuracy.txt').toString();

var n = 0;

function mean_accuracy(){
console.log("\ncalculating mean ..");
var part = data;
var x_acc = "";
var x_acc_sum = 0;
var x_mean_acc = 0;
var y_acc = "";
var y_acc_sum = 0;
var y_mean_acc = 0;

	while (part.indexOf('.') != -1){
		n++;
		console.log("reading "+n);
		x_acc = part.substring(part.indexOf('.')-1,part.indexOf(',')-1);
		x_acc_sum = x_acc_sum + parseFloat(x_acc);
		x_mean_acc = x_acc_sum/n;
		part = part.substring(part.indexOf(','));
		y_acc = part.substring((part.indexOf('.')-1),part.indexOf('\n')-1);
		y_acc_sum = y_acc_sum + parseFloat(y_acc);
		y_mean_acc = y_acc_sum/n;
		part = part.substring(part.indexOf('\n'));
	}
var mean_acc = [x_mean_acc,y_mean_acc];
return mean_acc;
}

function acc_variance(mean,no_of_samples){
console.log("\ncalculating variance ..");
var part = data;
var x_acc = "";
var x_variance = 0;
var y_acc = "";
var y_variance = 0;
	while (part.indexOf('.') != -1){
		x_acc = part.substring(part.indexOf('.')-1,part.indexOf(',')-1);
		x_variance = x_variance + (Math.pow(mean[0] - parseFloat(x_acc),2)/no_of_samples);
		part = part.substring(part.indexOf(','));
		y_acc = part.substring((part.indexOf('.')-1),part.indexOf('\n')-1);
		y_variance = y_variance + (Math.pow(mean[1] - parseFloat(y_acc),2)/no_of_samples);
		part = part.substring(part.indexOf('\n'));
	}
var variance = [x_variance,y_variance];
return variance;
}

var mean = mean_accuracy();
console.log('\nx accuracy mean = '+mean[0]+'\ny accuracy mean = '+mean[1]);
console.log('\nno of samples is '+n);
var variance = acc_variance(mean,n);
console.log('\nx accuracy variance = '+variance[0]+'\ny accuracy variance = '+variance[1]);
console.log('\nx accuracy std. dev. = '+Math.sqrt(variance[0])+'\ny accuracy std. dev. = '+Math.sqrt(variance[1]));
