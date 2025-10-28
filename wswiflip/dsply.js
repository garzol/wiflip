
const p1Elem = ["p1-0", "p1-1", "p1-2", "p1-3", "p1-4", "p1-5"];
const p2Elem = ["p2-0", "p2-1", "p2-2", "p2-3", "p2-4", "p2-5"];
const p3Elem = ["p3-0", "p3-1", "p3-2", "p3-3", "p3-4", "p3-5"];
const p4Elem = ["p4-0", "p4-1", "p4-2", "p4-3", "p4-4", "p4-5"];
const fpElem = ["fp-0", "fp-1"];
const crElem = ["cr-0", "cr-1"];
const ltElem = ["ltry-0", "ltry-1"];


function sevenseg2value(inval) {
	switch(inval) {
		case 0:
			return(-1);
		case 6:
			return(1);
		
		case 7:
			return(7);
			
		case 63:
			return(0);
		case 79:
			return(3);
		case 91:
			return(2);
		case 102:
			return(4);
			case 109:
				return(5);
		case 111:
			return(9);
		case 125:
			return(6);
			
		case 127:
			return(8);
		default:
			return(14);
		
	}
	
}


function dsplf0(d, eId) {
	const container = document.getElementById(eId);
	if (d==-1) {
		container.innerHTML = "&nbsp;";	
		return;	
		
	}
	try {
		const d0 = d&0x0F;
		container.innerHTML = d0.toString(16).toUpperCase();//parseInt(d, 16);		
	}
	catch(err) {
		console.debug(err, d, eId);
		
	}
}

function affdspl(typ, data) {
	

	if (typ==65) {
		const aff1 =[~data[4]&0x0F, (~data[4]&0xF0)>>4,
				     ~data[3]&0x0F, (~data[3]&0xF0)>>4, 
					 ~data[2]&0x0F, 0];
					 
		//const p1_Elem = document.getElementById("tableau-1");
		for (let i=0; i<aff1.length; i++) {
			dsplf(aff1[i], p1Elem[i])
		}
		const aff2 = [~data[8]&0x0F, (~data[8]&0xF0)>>4,
				      ~data[7]&0x0F, (~data[7]&0xF0)>>4, 
					  ~data[6]&0x0F, 0];
					 
		//const p1_Elem = document.getElementById("tableau-1");
		for (let i=0; i<aff2.length; i++) {
			dsplf(aff2[i], p2Elem[i])
		}
		
		const afffp = [(~data[1]&0xF0)>>4, ~data[1]&0x0F];
		for (let i=0; i<afffp.length; i++) {
			dsplf(afffp[i], fpElem[i])
		}

				
//		#ball in play + game over
//		bstat = (data[5]&0x70)>>4
//		bstat = bstat ^ 0b0111
		var bstat = (data[5]&0x70)>>4;
		bstat     = bstat ^ 0b0111;
		for (let i=0; i<5; i++) {
			let container = document.getElementById("bip-"+(i+1));
			if (bstat==i) {
				container.classList.remove('invisible');
				container.classList.add('visible');				
			}
			else {
				container.classList.remove('visible');
				container.classList.add('invisible');								
			}
		}
		
		//game over
		const goElem = document.getElementById("bip-go");
		if (bstat == 7) {
			goElem.classList.remove('invisible');
			goElem.classList.add('visible');
		}
		else {
			goElem.classList.add('invisible');
			goElem.classList.remove('visible');
			
		}
		//tilt
		const tiltElem = document.getElementById("bip-tilt");
		if ((~data[5]&0x80)) {
			tiltElem.classList.remove('invisible');
			tiltElem.classList.add('visible');
		}
		else {
			tiltElem.classList.add('invisible');
			tiltElem.classList.remove('visible');
			
		}
		
		//lottery
		const affltry = [~data[5]&0x0F, 0];
		for (let i=0; i<affltry.length; i++) {
			dsplf(affltry[i], ltElem[i]);
		}
		
		//leds player 1, 2
		dspll((data[2]&0xF0)>>4, ["p1-1M", "p1-l1", "p1-l2", "p1-d1"]);
	    dspll((data[6]&0xF0)>>4, ["p2-1M", "p2-l1", "p2-l2", "p2-d1"]);
	}
	

	
	else if (typ==66) {
		const aff4 =[~data[4]&0x0F, (~data[4]&0xF0)>>4,
				     ~data[3]&0x0F, (~data[3]&0xF0)>>4, 
					 ~data[2]&0x0F, 0];
					 
		//const p1_Elem = document.getElementById("tableau-1");
		for (let i=0; i<aff4.length; i++) {
			dsplf(aff4[i], p4Elem[i])
		}
		const aff3 = [~data[8]&0x0F, (~data[8]&0xF0)>>4,
				      ~data[7]&0x0F, (~data[7]&0xF0)>>4, 
					  ~data[6]&0x0F, 0];
					 
		//const p1_Elem = document.getElementById("tableau-1");
		for (let i=0; i<aff3.length; i++) {
			dsplf(aff3[i], p3Elem[i])
		}		

		const affcr = [(~data[1]&0xF0)>>4, ~data[1]&0x0F];
		for (let i=0; i<affcr.length; i++) {
			dsplf(affcr[i], crElem[i])
		}

		//leds player 4, 3
		dspll((data[2]&0xF0)>>4, ["p4-1M", "p4-l1", "p4-l2", "p4-d1"]);
		dspll((data[6]&0xF0)>>4, ["p3-1M", "p3-l1", "p3-l2", "p3-d1"]);
		
				
	}
	function dsplf(d, eId) {
		const container = document.getElementById(eId);
		if (d==15)
			container.innerHTML = "&nbsp;";
		else
			container.innerHTML = d.toString(16).toUpperCase();//parseInt(d, 16);
	}



	function dspll(d, teId) {
		let container1M = document.getElementById(teId[0]);
		if (!(d&0b0100)) {
			container1M.innerHTML = 1;			
		}
		else {
			container1M.innerHTML = "";						
		}
		let containerl1 = document.getElementById(teId[1]);
		if (!(d&0b0001)) {
			containerl1.setAttribute("class", "miniled led-red");
			}
		else {
			containerl1.setAttribute("class", "miniled led-black border border-3");
			}
		let containerl2 = document.getElementById(teId[2]);
		if (!(d&0b0010)) {
			containerl2.setAttribute("class", "miniled led-red");
			}
		else {
			containerl2.setAttribute("class", "miniled led-black border border-3");
			}
		const collection = document.querySelectorAll('.'+teId[3]);
		//const collection = document.getElementsByClassName(teId[3]);
		//console.log(collection);
		if (!(d&0b1000)) {
			collection.forEach(elem => { elem.classList.remove('invisible');
				                         elem.classList.add('visible');
										 });
		}
		else {
			collection.forEach(elem => { elem.classList.remove('visible');
				                         elem.classList.add('invisible');
										 });
		}
		
		//Now for each digit, turn dot off if digit value is F
		for (let nd=0; nd<5; nd++) {
			for (let np=1; np<5; np++) {
				let elemDigitId = "p"+np+"-"+nd;
				let elemDotId   = "p"+np+"-d1-"+nd;
				let elemDigit   = document.getElementById(elemDigitId);
			    let elemDot     = document.getElementById(elemDotId);
				//console.log(nd+' '+np+' '+elemDigit.textContent)
				if (!elemDigit.innerHTML ||
					 elemDigit.innerHTML=="&nbsp;") {
					elemDot.classList.remove('visible');
					elemDot.classList.add('invisible');
				}
			}
		}

	}

}
	
