

//Globals of the js application
//const event = new CustomEvent("build", { detail: elem.dataset.time });

function checkIp(ip) {
    const ipv4 = 
        /^(\d{1,3}\.){3}\d{1,3}$/;
    const ipv6 = 
        /^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/;
    return ipv4.test(ip) || ipv6.test(ip);
}


function initsys(){

}

function fletcher(arr) {
	var C0 = 0;
	var C1 = 0;
	
	for (let i in arr) {
		C0 = ( (C0+arr[i]) % 255 );
		C1 = ( (C0 + C1)   % 255 );
	}
	
	let ret = C1*256+C0;

	return ret;
}   


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


async function myRequest(message, sigTyp) {
  let myPromise = 	new Promise(function(resolve, reject) {
	   window.addEventListener(sigTyp, AckReceived);
	   const myTimeout = setTimeout(myGreeting, 3000);
	   sendmsg_onclick(message);
	
	   function AckReceived(e) {
	   	window.removeEventListener(sigTyp, AckReceived);	
		clearTimeout(myTimeout);
	   	//console.log("in ack received");	
		framer = e.detail;
		resolve(framer);	   	
	   }
	   function myGreeting() {
	   	window.removeEventListener(sigTyp, AckReceived);		
	   	console.log("in myGreeting");	
	   	reject("Timeout");
	   	return;
	   	
	   }
 
	   //setTimeout(function(reject) {reject("Garzol");}, 3000);
	  });

	//YR0XX pour lire sys mem 128 bytes
	//const b1 = new Uint8Array(message);

	//sendmsg_onclick(b1);

	const resul = await myPromise;
	console.log(resul);
	
	return(resul);



}



//Transform a bytes array to a nibble array
//Using yield pour la frime
function* b2n(bbytes) {
for (var i in bbytes) {
    let val = {l: bbytes[i]&0x0F, h:bbytes[i]>>4};
	for (var k in val) {
    	yield val[k];
        }
        
	}
}

//Transform a nibble array to a byte array
//Using yield pour la frime
// no problemo of parity: the size of bnibbles is even for sure because
//it was made from b2n
function* n2b(bnibbles) {
for (var ix=0; ix<bnibbles.length; ix+=2) {
    let val = bnibbles[ix] + (bnibbles[ix+1]<<4)
    yield val;        
	}
}



//TToastin'
function displayToast(txt1, txt2) {
	const mytoast = document.getElementById("liveToast");
	var toast = new bootstrap.Toast(mytoast);
	const mytoastT0 = document.getElementById("imgTitle-toastId");
	mytoastT0.innerHTML = "spider.pps4.fr";	
	const mytoastT1 = document.getElementById("timeInfo-toastId");
	mytoastT1.innerHTML = txt1;
	const mytoastT2 = document.getElementById("main-toastId");
	mytoastT2.innerHTML = txt2;
	
	toast.show();
	
}

