var IOTA = require('../lib/iota');
var Signing = require('../lib/crypto/signing/signing');
var Converter = require('../lib/crypto/converter/converter');
var Utils = require('../lib/utils/utils')
var crypto = require("crypto");
var fs = require('fs');
var rl = require('readline-sync');

//	オフラインでも動く。
var iota = new IOTA();

//	seedを入力する。
const seeds = function(){
	obj = {};

	var numOfSeed = rl.questionInt('いくつのSeedを使用しますか? ( 1 以上): ');

	if(numOfSeed < 1){
		return null;
	}

	obj.seeds = [];

	var seed,security;
	for(var i = 0;i<numOfSeed;i++){
		seed = rl.questionNewPassword('Seed: ',{charlist:'$<A-Z>9',mask:'#',min:81,max:81});
        security = rl.questionInt('Security(1~3): ');

        if(security < 1){
        	return null;
        }

        obj.seeds.push({"seed":seed,"security":security});

        console.log('- Seedは必ずオフラインで保管しましょう。');
	}

	obj.index = rl.questionInt('current index: ');

	if(obj.index < 0){
		return null;
	}

	return obj;
}

//	アドレスを作成する。
const next = function(login,currentIndex){
	var digestList = [];
	login.seeds.forEach(function(each){
		digestList.push(iota.multisig.getDigest(each.seed, currentIndex, each.security));
	});

	var Address = iota.multisig.address;

	var d = '';
	digestList.forEach(function(each){
		d += each;
	});

	var digests = Converter.trits(d);
	var address = Converter.trytes(Signing.address(digests));

	//	生成されたアドレスは有効か確認。
	var isValid = iota.multisig.validateAddress(address, digestList);
	if(isValid){
		console.log('- - - - - - - - - - - - - - - - - - - - ');
		console.log(' - index              : ',currentIndex);
		console.log(' - address            : ',address);
		console.log(' - address + checksum : ',Utils.addChecksum(address));
		console.log('- - - - - - - - - - - - - - - - - - - - ');
	}else{
		console.log('Error: Invalid address.');
	}
}

var login = seeds();

if(login != null){
	var index = login.index;
	while(true){
		next(login,index);
		if(!rl.keyInYN('Want next index?')){
			break; 
		}
		index++;
	}
}else{
	console.log('Error: Invalid infomation input.');
}


