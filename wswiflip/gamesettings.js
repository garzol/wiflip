//ishex writing

var nb_open_gtab = 0;
var tabEl = document.querySelectorAll('a[data-bs-toggle="tab"]')
//console.log(tabEl)
for (i = 0; i < tabEl.length; i++) {
  tabEl[i].addEventListener('shown.bs.tab', function(event) {
    //const activated_pane = event.target;
    //const deactivated_pane = event.relatedTarget;

//	console.log(event.target.href);
//	console.log(event.relatedTarget.href);
//	
//	console.log(activated_pane.id)
//    console.log(deactivated_pane.id)

    if (event.target.id == "htab-game-settings-Id") {
		populategsData();
	
	    if (!nb_open_gtab) {
			nb_open_gtab++;
			buildFlexiTable();
			make_tables_resizeable("flexicol");
		}
	}
    // do stuff
    //activated_pane.append(' hello ' + activated_pane.id)

  })
}


const selBpPArr = {option: {"8": "3 balls per play", "0": "5 balls per play"}};	
const selCnRArr = {option: {"0": "1 Play per Coin", "1": "2 Plays per Coin", "2": "3 Plays per Coin", "3": "4 Plays per Coin",}};	
const selCrRArr = {option: {"0": "2 Coins", "4": "1 Coin",}};	
const selPrTArr = {option: {"0": "Normal Price", "8": "Premium Price",}};	
const selEbMArr = {option: {"0": "Extra Ball not Repetitive", "1": "Extra Ball Repetitive", "2": "Extra Ball Accumulative"}};	
const selFpMArr = {option: {"0": "Free Play not Repetitive", "4": "Free Play Repetitive",}};	

const ttbprn = "Production number on 5 hex digits. This value can be altered through this interface. To retrieve \
the factory production number of the board, just click the factory reset button in the system settings tab.";
const ttbmdl = "Model number on 4 bcd digits. \
This value is automatically refreshed by the system when a reprogramming is done. <br>Several games have a forgotten Model number. <br> \
Please contact us at www.pps4.fr/contact/ if you know the original number.";
const ttbsnp = "Serial Number of last miniprinter used";
const ttbcrl = "Maximum credit: 0 for max. 09 credits, 1 for max 19, 2 for max 29, etc...";

const tthhp1 = "1st handicap (High score to date: 1M + param x10 (Player #1)";
const tthhp2 = "2nd handicap (High score to date: 1M + param x10 (Player #2)";
const tthhp3 = "3rd handicap (High score to date: 1M + param x10 (Player #3)";
const tthhp4 = "4th handicap (High score to date: 1M + param x10 (Player #4)";

const ttcprt = "Premium price: 1 Extra Play with 2nd payment (min. 1 play) \
WITHOUT PRESSING THE START BUTTON \
(This state affects all 3 coin rejectors)";

const ttvadj ="This is a 2-hex value whose meaning is dependent of the current programmed game. \
Read the corresponding operating manual to get the exact meaning of these fields.\
In general, the second digit is used to determine if bonuses are incremented by 1 or by 2.";

const gameSettingsArr = 
	
	{"Basics" : [
		{name: "Production N°",       toolTip: ttbprn,        type: "hex",  addr: {ptr: 0x2B, lnbl: 5, fmt:"hex", dir: -1},          content: {placeholder: "23BC4"}    },
		{name: "Model N°",            toolTip: ttbmdl,        type: "hex",  addr: {ptr: 0x24, lnbl: 4, fmt:"bcd", dir: -1},          content: {placeholder: "1053"}    },
		{name: "Serial N° of Printer",toolTip: ttbsnp,        type: "hex",  addr: {ptr: 0x1B, lnbl: 5, fmt:"hex", dir: -1},          content: {placeholder: "23BC4"}    },
		{name: "Credit Limit",        toolTip: ttbcrl,        type: "hex",  addr: {ptr: 0x20, lnbl: 1, fmt:"bcd", dir: -1},          content: {placeholder: "1"}    },

	],	
		
	"Score Threshold" : [
		{name: "Extra ball",          type: "hex",  addr: {ptr: 0x80, lnbl: 2, fmt:"bcd", dir: 1},       content: {placeholder: "44"}       },
		{name: "1st Freeplay",        type: "hex",  addr: {ptr: 0x60, lnbl: 2, fmt:"bcd", dir: 1},       content: {placeholder: "65"}       },
		{name: "2nd Freeplay",        type: "hex",  addr: {ptr: 0x70, lnbl: 2, fmt:"bcd", dir: 1},       content: {placeholder: "91"}       },
		
	],
	
	"Initial Contents" : [
		{name: "#Credit",          type: "hex",  addr: {ptr: 0x50, lnbl: 2, fmt:"bcd", dir: 1},       content: {placeholder: "15"}       },
		{name: "#Replay",          type: "hex",  addr: {ptr: 0x40, lnbl: 1, fmt:"bcd", dir: 1},       content: {placeholder: "0"}       },
		{name: "#Extra Ball",      type: "hex",  addr: {ptr: 0x41, lnbl: 1, fmt:"bcd", dir: 1},       content: {placeholder: "0"}       },

		],

	"Game Variant" : [
			{name: "Adj. Play", toolTip: ttvadj, type: "hex",  addr: {ptr: 0x90, lnbl: 2, fmt:"hex", dir: -1},       content: {placeholder: "3F"}       },

			],

	"Handicaps" : [
		{name: "#Handicap #1", toolTip: tthhp1,      type: "hex",  addr: {ptr: 0x63, lnbl: 5, fmt:"bcd", dir: -1},          content: {placeholder: "00000"}    },
	    {name: "#Handicap #2", toolTip: tthhp2,      type: "hex",  addr: {ptr: 0x6B, lnbl: 5, fmt:"bcd", dir: -1},          content: {placeholder: "00000"}    },
        {name: "#Handicap #3", toolTip: tthhp3,      type: "hex",  addr: {ptr: 0x7B, lnbl: 5, fmt:"bcd", dir: -1},          content: {placeholder: "00000"}    },
        {name: "#Handicap #4", toolTip: tthhp4,      type: "hex",  addr: {ptr: 0x73, lnbl: 5, fmt:"bcd", dir: -1},          content: {placeholder: "00000"}    },
	],	

	"Coin Logic" : [
			{name: "1st Coin Rejector",            type: "sel",  addr: {ptr: 0xA0, lnbl: 1, msk: 0x3, dir: 1},        content: selCnRArr   },
			{name: "2nd Coin Rejector",            type: "sel",  addr: {ptr: 0xA1, lnbl: 1, msk: 0x3, dir: 1},        content: selCnRArr   },
			{name: "3rd Coin Rejector",            type: "hex",  addr: {ptr: 0xB0, lnbl: 1, fmt:"bcd", dir: 1},       content: {placeholder: "1"}       },
			{name: "1st Coin Rejector - #Coins",   type: "sel",  addr: {ptr: 0xA0, lnbl: 1, msk: 0x4, dir: 1},        content: selCrRArr   },
			//following option is a mistake. Never existed 2025-10-11
			//{name: "2nd Coin Rejector - #Coins",   type: "sel",  addr: {ptr: 0xA1, lnbl: 1, msk: 0x4, dir: 1},        content: selCrRArr   },
			{name: "Price Type", toolTip: ttcprt,  type: "sel",  addr: {ptr: 0xA1, lnbl: 1, msk: 0x8, dir: 1},        content: selPrTArr   },

			],
		
	"Mode of Play" : [
		{name: "Balls per Play",      type: "sel",  addr: {ptr: 0xB1, lnbl: 1, msk: 0x8, dir: 1},         content: selBpPArr   },
		{name: "E.B. Mode",           type: "sel",  addr: {ptr: 0xB1, lnbl: 1, msk: 0x3, dir: 1},         content: selEbMArr   },
		{name: "F.P. Mode",           type: "sel",  addr: {ptr: 0xB1, lnbl: 1, msk: 0x4, dir: 1},         content: selFpMArr   },
		
	]

	};

	
//addr: {ptr: 0x63, lnbl: 5, fmt:"bcd", dir: -1},		
function isHex(value, template) {
	//const userKeyRegExp = /^[A-Z]\-[0-9]{2}\-[0-9]{2}[A-Z]?$/;

	//const pattern_bcd = /^[0-9]{0,5}$/i;

	const lnbl   = template.lnbl;
	const subfmt = template.fmt; //hex or bcd
	const re_hex = new RegExp(String.raw`^([0-9]|[A-F]){0,${lnbl}}$`, "i");
	const re_bcd = new RegExp(String.raw`^[0-9]{0,${lnbl}}$`, "i");

	
	const valid  = (subfmt=="bcd") ? re_bcd.test(value) : re_hex.test(value);

	
	//console.log("ishex", value, valid);	

	return valid;	
}

//addr: {ptr: 0xB1, lnbl: 1, msk: 0x8, dir: 1}, 
function isSel(value, template) {
	const mask = template.addr.msk;
	const keys = Object.keys(template.content.option);
	
	//console.log(keys, value);
	return(keys.includes(String(value)));
	
}

function reflectValidity(obj, valid)
{
	if (valid) {
		obj.classList.add("bg-success");
		obj.classList.add("text-white");
		obj.classList.remove("bg-danger");
	}
	else {
		obj.classList.add("bg-danger");
		obj.classList.add("text-white");
		obj.classList.remove("bg-success");
		
	}

}
function validateField(e) {
	const valid = isHex(e.currentTarget.value, e.currentTarget.fmt);
    reflectValidity(e.currentTarget, valid);	
}

var nvrNblFrame;
function writeSelHex(obj) {
	const lnbl   = obj.addr.lnbl;
	const dir    = obj.addr.dir;
	const addr   = obj.addr.ptr;
	
	const value  = obj.elem.value;
	if (obj.type == "hex") {
		var nbl_resul = new Uint8Array(lnbl).fill(0);
		
		for (let i=0; i<obj.elem.value.length; i++) {
			nbl_resul[i+ (lnbl-obj.elem.value.length)] = Number("0x"+obj.elem.value[i].toString(16));			
			}
		if (dir != 1)
			nbl_resul = nbl_resul.reverse();
		
		//console.log(obj.name, typeof(addr), addr, nbl_resul);
		for (let i=0; i<nbl_resul.length; i++) {
			nvrNblFrame[addr+i] = nbl_resul[i];
			//console.log("nvrNblFrame de i ", addr+i, nvrNblFrame[addr+i])
		}
	}
	else if (obj.type == "sel") {
		//  nibbles[addr] = (nibbles[addr] & (~bitMask)) | targetValue
		const bitMask = obj.addr.msk;
		nvrNblFrame[addr] = (nvrNblFrame[addr] & (~bitMask)) | value;
		//console.log("set sel", obj.name, bitMask, value, addr, nvrNblFrame[addr]);
	}
    //console.log("nvrNblFrame inside", nvrNblFrame);
}

function checkandwriteGS() {
	const  modalTitleElem= document.getElementById("modal-title-id");
	const  modalBodyElem= document.getElementById("modal-body-id");
	const  modalButtonElem= document.getElementById("modal-button-id");

	const modalElem = document.getElementById("reprog-myModal");
	var myModal = new bootstrap.Modal(modalElem, {
	  keyboard: true
	});

	
	var errorsArr = new Array();
	for (let category in gameSettingsArr) {
		for (let i in gameSettingsArr[category]) {
			switch(gameSettingsArr[category][i].type) {
				case "hex":
					if (!isHex(gameSettingsArr[category][i].elem.value, gameSettingsArr[category][i].addr)) {
						errorsArr.push(category+": "+gameSettingsArr[category][i].name);
					}
					break;
				case "sel":
					if (!isSel(gameSettingsArr[category][i].elem.value, gameSettingsArr[category][i])) {
						errorsArr.push(category+": "+gameSettingsArr[category][i].name);
					}
					break;
				default:
					break;
								
			}
		}
	}	
	//console.log(errorsArr);
	var txt="";
	if (errorsArr.length) {
		for (obj of errorsArr) {
			txt += obj+"<br>";
		}
		modalButtonElem.classList.add("bg-danger");					
		modalButtonElem.classList.remove("bg-success");					
		modalTitleElem.innerHTML = "Game settings not modified";
		modalBodyElem.innerHTML  = "Fix the following fields first:<br> "+txt;
		myModal.show();
		return;
		
	}
	writeGSAll();
}
//write all game settings to the device
async function writeGSAll() {

	const  modalTitleElem= document.getElementById("modal-title-id");
	const  modalBodyElem= document.getElementById("modal-body-id");
	const  modalButtonElem= document.getElementById("modal-button-id");

	const modalElem = document.getElementById("reprog-myModal");
	var myModal = new bootstrap.Modal(modalElem, {
	  keyboard: true
	});

	nvrNblFrame = new Uint8Array([...b2n(nvrFrame)]);
	
	//console.log("nvrFrame brut", typeof(nvrFrame), nvrFrame);
	//console.log("duplic", duplic);
	//console.log("nvrNblFrame", nvrNblFrame.map(function (x) {return x.toString(16)}));
	
	for (let category in gameSettingsArr) {
		for (let i in gameSettingsArr[category]) {
			writeSelHex(gameSettingsArr[category][i]);
			}
    }	
	
	const nvrFrameMod = new Uint8Array([...n2b(nvrNblFrame)]);
	//console.log("nvrNblFrame", nvrNblFrame);
	//console.log("nvrFrame brut", nvrFrame);
	//console.log("nvrFrame mod ", nvrFrameMod);
	
	var changeCnt = 0;
	for (let ix=0; ix<nvrFrame.length; ix++) {
		if (nvrFrame[ix] != nvrFrameMod[ix]) {
			changeCnt++;
			let memtyp = 1; //nvram
			let addr = ix;
			let msg = new Uint8Array([89, 87, memtyp, addr, nvrFrameMod[ix]]);	
			//console.log("writing", nvrFrame[ix], nvrFrameMod[ix], ix, msg);
			sendmsg_onclick(msg);
		}
	}
	await sleep(200);
	
	if (!changeCnt) {
		displayToast("Now", "Nothing to do. Doing nothing.");
		return;			
	}
	let flashgsettings = new Uint8Array([89, 70, 1, 88, 88]);
	sendmsg_onclick(flashgsettings);
	await sleep(600);
	
//	//reset
//	let resetmsg = new Uint8Array([89, 67, 88, 81, 90]);
//	sendmsg_onclick(resetmsg);
	
//  right way to do an acknowledged reset:
    const resetmsg = new Uint8Array([89, 67, 88, 81, 90]);
	try {	
		resetAck = await myRequest(resetmsg, "ResetReceived");
	}
	catch(err) {
			modalButtonElem.classList.add("bg-danger");					
			modalButtonElem.classList.remove("bg-success");					
			modalTitleElem.innerHTML = "Game settings not modified";
			modalBodyElem.innerHTML  = "Failure. "+`${err} error. Device did not reply. Please check your connection and retry.<br>Abort`;
			myModal.show();
			return;		
		
	}
	
	displayToast("Now", "Changes Applied. Device is resetting...")	
	
}
function buildFlexiTable()
{
	var table = document.getElementById("game-settings-tableId");

	
	for (let category in gameSettingsArr) {
		var row = table.insertRow(-1);
		var cell1 = row.insertCell(0);
		const att_colspan = document.createAttribute("colspan");
		att_colspan.value = "2";
		cell1.setAttributeNode(att_colspan);
		//cell1.colspan = "2";    //Does not work!!!!
		cell1.style.textAlign = "center";
		cell1.innerHTML = category;
		cell1.style.fontStyle="italic";
		cell1.style.fontWeight="bolder";
		cell1.style.background="black";
		cell1.style.color="white";
		
		for (let i in gameSettingsArr[category]) {
			var row = table.insertRow(-1);
			var cell1 = row.insertCell(-1);
			//cell1.style.background = "lightgray";
			var ttp;
			try {
				ttp = gameSettingsArr[category][i].toolTip;
			}
			catch(err) {
				ttp = "nothing to declare";
			}
			if (ttp===undefined){
				ttp="";
			}
			//console.log("tt", ttp, ttp===undefined);
			
			cell1.style.textAlign = "right";
			if (!ttp) {
				cell1.innerHTML = gameSettingsArr[category][i].name + 
				                  `&nbsp;<i data-bs-toggle="tooltip"  
								  title="${ttp}" data-bs-html="true" 
								   class="bi bi-question-circle-fill text-muted"></i>&nbsp;`;
			}
			else {
				cell1.innerHTML = `<a >` +
								  gameSettingsArr[category][i].name + 
				                  `&nbsp;<i data-bs-toggle="tooltip"  
								  		title="${ttp}" data-bs-html="true" 
										data-bs-trigger="focus hover" 
										data-bs-template = '<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div style="min-width:350px" class="tooltip-inner bg-secondary text-start"></div></div>'
								  		class="bi bi-question-circle-fill"></i>&nbsp;</a>`;
				
			}
			var cell2 = row.insertCell(-1);
			//cell2.innerHTML = "Valueable";
			var cell2_content;
			switch(gameSettingsArr[category][i].type) {
				case "hex":
					cell2_content = document.createElement("textarea");
					//cell2_content.type="text";
					cell2_content.placeholder=gameSettingsArr[category][i].content.placeholder;
					cell2_content.cols=gameSettingsArr[category][i].content.placeholder.length;
					cell2_content.maxLength=gameSettingsArr[category][i].content.placeholder.length;
					cell2_content.rows="1";
					cell2_content.style.resize = "none";
					cell2_content.classList.add("w-100");  //bs5 class 
					cell2_content.classList.add("px-1");  //bs5 class 
					cell2_content.classList.add("mx-1");  //bs5 class 
					cell2_content.addEventListener("change", validateField);
					cell2_content.addEventListener("keydown", function(e) {
						if (e.key == "Enter") {
							//cell2.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Tab'}));
							//form.elements[index + 1].focus();
							e.preventDefault();
							//alert(e.key, form, index);
							//return true;

						}
					});
					
					cell2_content.fmt = gameSettingsArr[category][i].addr;
					gameSettingsArr[category][i].elem = cell2_content;
					break;
				case "sel":
					cell2_content = document.createElement("select");
					const att = document.createAttribute("class");
					att.value = "form-select form-select-sm";
					cell2_content.setAttributeNode(att);
					const option_list = gameSettingsArr[category][i].content.option;
					for (let opt in option_list) {
						let optElem = document.createElement("option");
						optElem.value = opt;
						let t = document.createTextNode(gameSettingsArr[category][i].content.option[opt]);
						optElem.appendChild(t);
						cell2_content.appendChild(optElem);
					}
					gameSettingsArr[category][i].elem = cell2_content;
					break;
			}
			cell2.appendChild(cell2_content);
		}
		
	}

	var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
	var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
	  return new bootstrap.Tooltip(tooltipTriggerEl)
	})
}
	
	
async function populategsData() {

	const  modalTitleElem= document.getElementById("modal-title-id");
	const  modalBodyElem= document.getElementById("modal-body-id");
	const  modalButtonElem= document.getElementById("modal-button-id");

	const modalElem = document.getElementById("reprog-myModal");
	var myModal = new bootstrap.Modal(modalElem, {
	  keyboard: true
	});
	
	const memtyp = 1; //nvr 128 bytes
	
	//read nvr  YR, memtyp=1, 
	try {	
		const nvrdata = await myRequest(new Uint8Array([89, 82, 1, 88, 88]), "DumpReceived");
		nvrFrame = nvrdata;
	}
	catch(err) {
			modalButtonElem.classList.add("bg-danger");					
			modalButtonElem.classList.remove("bg-success");					
			modalTitleElem.innerHTML = "Connection error";
			modalBodyElem.innerHTML  = "Failure. "+`${err} error. Device did not reply. Please check your connection and retry.<br>Abort`;
			myModal.show();
			return;		
		
	}

	//console.log("read nvr", nvrFrame);
	for (let category in gameSettingsArr) {
		for (let i in gameSettingsArr[category]) {
			//console.log(nvrFrame, nvrFrame);
			//console.log(category, gameSettingsArr[category][i].elem);
			//console.log("0x"+gameSettingsArr[category][i].addr.ptr.toString(16), nvrFrame[gameSettingsArr[category][i].addr.ptr]);
			switch (gameSettingsArr[category][i].type) {
				case "hex": {
					let nbl_addr = gameSettingsArr[category][i].addr.ptr;
					let nbl_len  = gameSettingsArr[category][i].addr.lnbl;   
					let nbl_dir  = gameSettingsArr[category][i].addr.dir;   
					let nbl_val  = buildGsData(nbl_addr, nbl_len, nbl_dir);
//					console.log(category, i, "0x"+(nbl_addr>>1).toString(16), nbl_val, "0x"+nvrFrame[nbl_addr>>1].toString(16));
//					console.log("a", gameSettingsArr[category][i]);
//					console.log("b", gameSettingsArr[category][i].elem);
//					console.log("c", gameSettingsArr[category][i].elem.value);
//					console.log("d", nbl_val);
					
					//try because elem may not exist at this stage
					try {
						gameSettingsArr[category][i].elem.value = nbl_val;	
						//const valid = isHex(nbl_val, gameSettingsArr[category][i].addr);
						let valid = isHex(nbl_val, gameSettingsArr[category][i].addr);
						reflectValidity(gameSettingsArr[category][i].elem, valid);
						}
					catch (err) {
						
						}
					}
					break;
				case "sel": {
					let nbl_addr  = gameSettingsArr[category][i].addr.ptr;
					let nbl_mask  = gameSettingsArr[category][i].addr.msk;
					let brut_val  = buildGsData(nbl_addr, 1, 1);
					let nbl_val   = Number("0x"+brut_val)&nbl_mask;
					
					try {
						gameSettingsArr[category][i].elem.value = nbl_val.toString(16);	
						//console.log(category, gameSettingsArr[category][i].name, i, "0x"+(nbl_addr>>1).toString(16), nbl_val, brut_val, "0x"+nvrFrame[nbl_addr>>1].toString(16));
						let valid = isSel(nbl_val, gameSettingsArr[category][i]);
						reflectValidity(gameSettingsArr[category][i].elem, valid);
						}
					catch (err) {
						
						}
					}
					break;
				default:
					break;
			}
		}
	}
	
	
}

function buildGsData(nbl_addr, nbl_len, nbl_dir) {
	
	var retval=String();
	var nbl_val;
	
	for (let i=0; i<nbl_len; i++) {
		let full_addr = (nbl_addr >> 1);
		let byte2    = nvrFrame[full_addr];
		if (nbl_addr % 2) {
			nbl_val = (byte2&0xF0)>>4;
		}
		else {
			nbl_val = byte2&0x0F;			
		}
		nbl_addr++;
		nbl_val = nbl_val.toString(16).toUpperCase();
		//console.log(i, String(nbl_val), byte2.toString(16), );
		if (nbl_dir == -1) {
			retval = String(nbl_val) + retval;						
		}
		else {
			retval = retval + String(nbl_val);			
		}
	}
	
	return(retval);
}