

//
//
const sc_mode_txtArr      = ["Factory reset", "Miniprinter", "Normal"];
var req_sc_flags1     = 0;
var sc_flags1         = 0;

const sysFlagsHmi = {
	"coin-rejector-optId"           : {"bit-num": 0,},
	"skip-coiltest-optId"           : {"bit-num": 1,},
	"standalone-switchmatrix-optId" : {"bit-num": 2,},
	"unprotect-coils-optId"         : {"bit-num": 3,},
};

function OnResetReceived(frameArray) {
    var evt = new CustomEvent('ResetReceived', { detail: frameArray });

    window.dispatchEvent(evt);
}
function OnDumpReceived(frameArray) {
    var evt = new CustomEvent('DumpReceived', { detail: frameArray });

    window.dispatchEvent(evt);
}
function OnFletcherReceived(frameArray) {
    var evt = new CustomEvent('FletcherReceived', { detail: frameArray });

    window.dispatchEvent(evt);
}

var sysFrame = new Uint8Array(128);  //memTyp=0
var nvrFrame = new Uint8Array(128);  //memTyp=1

async function memRequest(memTyp)
{
	  await sleep(500);
	  window.addEventListener('DumpReceived', memReceived);

	  //YR0XX pour lire sys mem 128 bytes
      const b1 = new Uint8Array([89, 82, memTyp, 88, 88]);

      sendmsg_onclick(b1);
	  const myTimeout = setTimeout(myGreeting, 2000);
	  function memReceived(e){
	  	//e.detail is frameArray that contains mem

	  	window.removeEventListener("DumpReceived", memReceived);
		clearTimeout(myTimeout);
		switch(memTyp) {
			case 1:
				nvrFrame = e.detail;
				console.log("update nvram local copy", nvrFrame);
				break;
			case 0:
				sysFrame = e.detail;
				
				
				const gcrcElement = document.getElementById("crc-cgId");
				const gnamElement = document.getElementById("name-cgId");
				const gmdlElement = document.getElementById("modl-cgId");
				
				const rcrcElement = document.getElementById("crc-crId");
				const rnamElement = document.getElementById("name-crId");
				
				
				
				//candidates_cg =  [x for x in RscPin.Models.keys() if RscPin.Models[x]["Game Fletcher"]==cg ]

				//requested vs current
				//current
				const cur_gcrc = Number("0x"+(sysFrame[24]+(sysFrame[25]<<8)).toString(16));
				const cur_rcrc = Number("0x"+(sysFrame[40]+(sysFrame[41]<<8)).toString(16));
				
				//requested				
				gcrcElement.setAttribute("value", "0x"+(sysFrame[16]+(sysFrame[17]<<8)).toString(16));
				rcrcElement.setAttribute("value", "0x"+(sysFrame[32]+(sysFrame[33]<<8)).toString(16));
				//update_text('dump sys config received: '+' '+sysFrame);
				//console.log(RscModelsArr);
				const candidates = RscModelsArr.filter(checkCRC, Number(gcrcElement.value));
				const cnames = candidates.map(el => el.name);
				gnamElement.setAttribute("value", cnames.join("/"));
				const cmdls = candidates.map(el => el.content["#Model"]);
				gmdlElement.setAttribute("value", cmdls.join("/"));
				
				const randidates = Bios.filter(checkCRC, Number(rcrcElement.value));
				const rnames = randidates.map(el => el.name);
				rnamElement.setAttribute("value", rnames.join("/"));
				
				if (cur_rcrc != Number(rcrcElement.value)) {
					rnamElement.classList.add("bg-danger");					
					rnamElement.classList.remove("bg-success");					
					
				}
				else {
					rnamElement.classList.add("bg-success");					
					rnamElement.classList.remove("bg-danger");					
				}
				if (cur_gcrc != Number(gcrcElement.value)) {
					gnamElement.classList.add("bg-danger");					
					gnamElement.classList.remove("bg-success");					
					
				}
				else {
					gnamElement.classList.add("bg-success");					
					gnamElement.classList.remove("bg-danger");					
					
				}
				
				//update select-game objects
				let elem1 = document.getElementById("game-select-reprog");
				elem1.value = cnames[0];
				let elem2 = document.getElementById("game-select");
				elem2.value = cnames[0];
				update_sm_labels(elem2)
				//update_text('rg: '+(sysFrame[16]+(sysFrame[17]<<8)).toString(16));
				//update_text('cg: '+(sysFrame[24]+(sysFrame[25]<<8)).toString(16));
				//update_text('rr: '+(sysFrame[32]+(sysFrame[33]<<8)).toString(16));
				//update_text('cr: '+(sysFrame[40]+(sysFrame[41]<<8)).toString(16));

				//update sys settings
//				sc_formatString =  f"{papa.nvrlist[0][1]:02X}"+f"{papa.nvrlist[1][1]:02X}"+f"{papa.nvrlist[2][1]:02X}"
//				sc_mode         =  papa.nvrlist[3][1]
//				sc_flags1       =  papa.nvrlist[4][1]
				
				const sc_formatString = sysFrame.subarray(0,3);
				const sc_mode         = sysFrame[3];
				sc_flags1             = sysFrame[4];
				req_sc_flags1         = sc_flags1;
				const applyButton = document.getElementById("sys-apply-btnId");	
				applyButton.setAttribute("disabled", "disabled");		

				update_text('format string: '+ sc_formatString[0].toString(16).toUpperCase()+
				                              sc_formatString[1].toString(16)+
											  sc_formatString[2].toString(16)

				            );
				update_text('Start mode: '+ sc_mode_txtArr[sc_mode]);
				//update_text('sc_flags1 '+sc_flags1);
				
				for (let i in sysFlagsHmi) {
					//console.log(i, sysFlagsHmi[i]);
					//console.log(sysFlagsHmi[i]["bit-num"]);
					let elem = document.getElementById(i);
					if (sc_flags1&(1<<sysFlagsHmi[i]["bit-num"])) {
						elem.checked = true;
					}
					else {
						elem.checked = false;						
					}
				}
				break;
			default:
				update_text('dump unknown received: '+e.detail);
				break;
		}
		
	  }

	  function myGreeting() {
	  	
	  	window.removeEventListener("DumpReceived", memReceived);
	  	update_text('Timeout error. The device did not reply to a memory dump request.');
	  	
	  }
}

function checkAddress(checkbox)
{
    const applyButton = document.getElementById("sys-apply-btnId");	
	
    if (checkbox.checked)
    {
        req_sc_flags1 |= (1<<sysFlagsHmi[checkbox.id]["bit-num"]);
    }
	else {
		req_sc_flags1 &= ~(1<<sysFlagsHmi[checkbox.id]["bit-num"]);		
	}
	//update_text(`sc_flag:${req_sc_flags1}`);
	
	if (req_sc_flags1 == sc_flags1) {
		applyButton.setAttribute("disabled", "disabled");		
	}
	else {
		applyButton.removeAttribute("disabled");
		
	}

}

async function applySysOptions()
{
	const memtyp = 0;
	const addr   = 4;
	const bbyt   = req_sc_flags1;


	//write flags to mem 0
	sendmsg_onclick(new Uint8Array([89, 87, memtyp, addr, bbyt]));
	
	await sleep(500);	    

	//flash memory 0
	sendmsg_onclick(new Uint8Array([89, 70, memtyp, 88, 88]));
	
	await sleep(500);	    

	//reset with ack
	let resetmsg = new Uint8Array([89, 67, 88, 81, 90]);
	sendmsg_onclick(resetmsg);

	
}
async function applySysFactory()
{
	const memtyp = 0;
	const addr   = 3;
	const bbyt   = 0; //0 factory settings, 1 miniprinter, 2 normal mode

	console.log("entering applysysfactory");

	//write flags to mem 0
	sendmsg_onclick(new Uint8Array([89, 87, memtyp, addr, bbyt]));
	
	await sleep(500);	    

	//flash memory 0
	sendmsg_onclick(new Uint8Array([89, 70, memtyp, 88, 88]));
	
	await sleep(500);	    

	//reset with ack
	let resetmsg = new Uint8Array([89, 67, 88, 81, 90]);
	sendmsg_onclick(resetmsg);

	console.log("factory done");
	
}
function checkCRC(model) {
	//const gcrcElement = document.getElementById("crc-cgId");
    //console.log(model.content, Number(gcrcElement.value));
	const refcrc = this;
	return model.content["Game Fletcher"] == refcrc;
}





async function start_reprog( ) {
	const gsElement = document.getElementById("game-select-reprog");
	const req_game = gsElement.options[ gsElement.selectedIndex ].value;
	//console.log(req_game);

	const  modalTitleElem= document.getElementById("modal-title-id");
	const  modalBodyElem= document.getElementById("modal-body-id");
	const  modalButtonElem= document.getElementById("modal-button-id");
	
	const modalElem = document.getElementById("reprog-myModal");
	var myModal = new bootstrap.Modal(modalElem, {
	  keyboard: true
	});

	gameFileName = RscModelsArr[gsElement.selectedIndex].content["Game bin"];
	//<!--<button onclick="sendmsg_onclick('YBXQR')">go into reprog mode</button>-->
	update_rconsole("Start programming ... ");
	sendmsg_onclick(new Uint8Array([89, 66, 88, 81, 82]));

	update_rconsole(`Loading game ${req_game}... `);
		
	const bin1024Arr = new Uint8Array(1024);
	
	var initialLength;
	try {
		initialLength = gameBin[gameFileName].length;
	} 
	catch {
		update_rconsole(`Error. ${gameFileName} not found. Abort<br>`);
		modalButtonElem.classList.add("bg-danger");					
		modalButtonElem.classList.remove("bg-success");					
		modalTitleElem.innerHTML = "Reprogramming failed";
		modalBodyElem.innerHTML  = "Failure. "+`Error. ${gameFileName} not found. Abort<br>`;
		myModal.show();
		return;
	}
	bin1024Arr.set(gameBin[gameFileName]);
	const binPadArr  = new Uint8Array(1024-initialLength);
	binPadArr.fill(0x81);
	bin1024Arr.set(binPadArr, initialLength);
	//console.log(bin1024Arr);
	await sleep(500);
	
	for (let addr in bin1024Arr) {
		let addrh  = (addr >> 4)&0xF0 
        let memTyp = 4;
		let msg = new Uint8Array([89, 87, addrh|memTyp, (addr&0xFF), bin1024Arr[addr]]);
		//console.log("send:",msg);
		sendmsg_onclick(msg);
		
	}	
	
	await sleep(200);
	
	const gameFletcher = fletcher(bin1024Arr);  //fletcher returns crc as an 'int'
	update_rconsole(`Sent Binary Game. Fletcher's: ${gameFletcher.toString(16)}`);
	await sleep(400);
	//update_text(`Sent Binary Game. Fletcher's: ${gameFletcher.toString(16)}`);
	
	var checkFletcher;
	try {	
		checkFletcher = await myRequest(new Uint8Array([89, 90, 4, 10, 88]), "FletcherReceived");
		//console.log(checkFletcher, "type",typeof checkFletcher);
		const hexcrc = "0x"+(checkFletcher[0]*256+checkFletcher[1]).toString(16);
		console.log("checker", hexcrc, checkFletcher);
		if (Number(hexcrc) != gameFletcher) {
			update_rconsole(`crc mismatch. Expected: ${gameFletcher.toString(16)}, received: ${hexcrc}. <br>Abort`);		
			modalButtonElem.classList.add("bg-danger");					
			modalButtonElem.classList.remove("bg-success");					
			modalTitleElem.innerHTML = "Reprogramming failed";
			modalBodyElem.innerHTML  = "Failure. "+`crc mismatch. Expected: ${gameFletcher.toString(16)}, received: ${hexcrc}. <br>Abort`;
			myModal.show();
			return;
			}
		
		update_rconsole(`Good game's fletcher received. ${hexcrc}. Now flashing...`);
	}
	catch(err) {
			update_rconsole(`${err} error. Device did not reply. Please check your connection and retry.`);		
			modalButtonElem.classList.add("bg-danger");					
			modalButtonElem.classList.remove("bg-success");					
			modalTitleElem.innerHTML = "Reprogramming failed";
			modalBodyElem.innerHTML  = "Failure. "+`${err} error. Device did not reply. Please check your connection and retry.<br>Abort`;
			myModal.show();
			return;		
		
	}
	
	await sleep(300);	
	//Flash game
	let flashgmsg = new Uint8Array([89, 70, 4, 88, 88]);
	//console.log("send:",msg);
	sendmsg_onclick(flashgmsg);
	await sleep(200);
	
	//write new crc
	let crclgmsg = new Uint8Array([89, 87, 0, 16, checkFletcher[1]]);
	sendmsg_onclick(crclgmsg);
	let crchgmsg = new Uint8Array([89, 87, 0, 17, checkFletcher[0]]);
	sendmsg_onclick(crchgmsg);
	await sleep(200);
	//and flash it
	let flashsys = new Uint8Array([89, 70, 0, 88, 88]);
	sendmsg_onclick(flashsys);
	await sleep(200);
	update_rconsole("Game flashed. <br>Now the system section (A1762 content)...");

	//load the system part
	const A1762FileName = RscModelsArr[gsElement.selectedIndex].content["A1762 bin"];
	
	const binA1762_1024Arr = new Uint8Array(gameBin[A1762FileName]);

	for (let addr in binA1762_1024Arr) {
		let addrh  = (addr >> 4)&0xF0 
	    let memTyp = 5;
		let msg = new Uint8Array([89, 87, addrh|memTyp, (addr&0xFF), binA1762_1024Arr[addr]]);
		//console.log("send:",msg);
		sendmsg_onclick(msg);
		
	}	
	
	await sleep(200);

	const sysFletcher = fletcher(binA1762_1024Arr);  //fletcher returns crc as an 'int'
	update_rconsole(`Sent Binary System part (${A1762FileName}). Fletcher's: ${sysFletcher.toString(16)}`);
	await sleep(200);
	
	var checksysFletcher;
	try {
		checksysFletcher = await myRequest(new Uint8Array([89, 90, 5, 10, 88]), "FletcherReceived");
		const hexsyscrc = "0x"+(checksysFletcher[0]*256+checksysFletcher[1]).toString(16);
		console.log("checker", hexsyscrc, checksysFletcher);
		if (Number(hexsyscrc) != sysFletcher) {
			update_rconsole(`Error. crc mismatch. Expected: ${sysFletcher.toString(16)}, received: ${hexsyscrc}<br>Abort`);		
			modalButtonElem.classList.add("bg-danger");					
			modalButtonElem.classList.remove("bg-success");					
			modalTitleElem.innerHTML = "Reprogramming failed";
			modalBodyElem.innerHTML  = "Failure. "+`crc mismatch. Expected: ${sysFletcher.toString(16)}, received: ${hexsyscrc}. <br>Abort`;
			myModal.show();
			return;
			}
		//Flash sys
		update_rconsole(`Good sys fletcher received. ${hexsyscrc}. Now flashing...`);
	}
	catch(err) {
		update_rconsole(`${err} error. Device did not reply. Please check your connection and retry.`);		
		modalButtonElem.classList.add("bg-danger");					
		modalButtonElem.classList.remove("bg-success");					
		modalTitleElem.innerHTML = "Reprogramming failed";
		modalBodyElem.innerHTML  = "Failure. "+`${err} error. Device did not reply. Please check your connection and retry.<br>Abort`;
		myModal.show();
		return;		
	}
	let flashsmsg = new Uint8Array([89, 70, 5, 88, 88]);
	//console.log("send:",msg);
	sendmsg_onclick(flashsmsg);
	await sleep(200);
	
	//write new crc
	let crclsmsg = new Uint8Array([89, 87, 0, 32, checksysFletcher[1]]);
	sendmsg_onclick(crclsmsg);
	let crchsmsg = new Uint8Array([89, 87, 0, 33, checksysFletcher[0]]);
	sendmsg_onclick(crchsmsg);
	await sleep(200);
	//and flash it
	//let flashsys = new Uint8Array([89, 70, 0, 88, 88]);
	sendmsg_onclick(flashsys);
	await sleep(200);
	update_rconsole("Sys flashed. <br>Now register the model number...");

	//register the model number
	let memtyp = 1 //#NVRAM
	let addr = 0x12  
	let model = RscModelsArr[gsElement.selectedIndex].content["#Model"];   
	for (let i=1; i>-1; i--) {
			let byte = (Number(model[2*i].toString(16)<<4)+
			            Number(model[2*i+1].toString(16)));		
		    let msg = new Uint8Array([89, 87, memtyp, addr, byte]);	
			console.log(i, model, addr, msg);
			sendmsg_onclick(msg);
			addr++;
	}
	await sleep(200);
	let flashgsettings = new Uint8Array([89, 70, 1, 88, 88]);
	sendmsg_onclick(flashgsettings);
	update_rconsole(`Model number (${model}) registered.`);
	await sleep(600);
	//reset
	let resetmsg = new Uint8Array([89, 67, 88, 81, 90]);
	sendmsg_onclick(resetmsg);
	update_rconsole("Programming successful. Resetting.<br>");
	
	  
	modalButtonElem.classList.add("bg-success");					
	modalButtonElem.classList.remove("bg-danger");					
	modalTitleElem.innerHTML = "Reprogramming done";
	modalBodyElem.innerHTML  = "Success";
	myModal.show();
}