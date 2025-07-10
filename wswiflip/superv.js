



var stored_dsplA = new Array(16).fill(0xC);
var stored_dsplB = new Array(16).fill(0xB);
try {
	console.log("array A storage is", JSON.parse(localStorage.stored_dsplA));
	stored_dsplA = JSON.parse(localStorage.stored_dsplA);	
	console.log("array A storage is now", stored_dsplA);
	
}
catch (err) {
	console.debug("array A store not set", err);
	localStorage.setItem("stored_dsplA", JSON.stringify(stored_dsplA));

}
try {
	console.log("array B storage is", JSON.parse(localStorage.stored_dsplB));
	stored_dsplB = JSON.parse(localStorage.stored_dsplB);	
    console.log("array B storage is now", stored_dsplB);
}
catch (err) {
	console.debug("array B store not set", err);
	localStorage.setItem("stored_dsplB", JSON.stringify(stored_dsplB));

}
var stored_items = {"dsplA": stored_dsplA, "dsplB": stored_dsplB};

const super_mycmds = {"dsplA":0x5A, "dsplB":0x5B, 
               "B2":0x20,        "B3-AB":0x30, 
               "B3-CD":0x31,     "B3-EF":0x32};

//super_gb is an array of array of objects
var super_gb = new Object();


function create_dsplSuper(typD) {

	const dsplXElement = document.getElementById(typD+"-superId");
	if (!dsplXElement) return;
	var super_gbx = new Object();
	super_gb[typD] = super_gbx;
	super_gbx.element = new Array();
	for (let i=0; i<16; i++) {
		var txtx_container = document.createElement("textarea");
		//txtx_container.value = i.toString(16).toUpperCase();
		var val;
		try {
			val = stored_items[typD][i].toString(16).toUpperCase();
			}
		catch (err) {
			stored_items[typD][i] = 0x0F;
			val = "F";
					}
		finally {
			txtx_container.value = val;
		}
		//var t = document.createTextNode(i.toString(16).toUpperCase());
		//txtx_container.appendChild(t);
		//txtx_container.textContent = txtx_container.value;
		txtx_container.maxLength = 1;
		txtx_container.classList.add("m-1")
		txtx_container.classList.add("text-center")
		txtx_container.classList.add("text-uppercase")
		txtx_container.classList.add("font-monospace")
		//txtx_container.style.height = txtx_container.scrollHeight + "px";
		txtx_container.style.width = "32px";
		txtx_container.style.height = "32px";
		txtx_container.style.overflowY = "hidden";
		txtx_container.style.overflowX = "hidden";
		txtx_container.style.resize = "none";
		txtx_container.title = "my title de bouffon";
		dsplXElement.appendChild(txtx_container);
		
		var elem = new Object({container:txtx_container});
		super_gbx.element.push(elem);
	    
		txtx_container.addEventListener("keypress", function(event) {
			var val = this.value;
			var validaterror = document.getElementById(typD+'-errorvalidate');
		    console.log(event.which, val);
				if (event.which == 13) {
					event.preventDefault();
					console.log("inside");
			    if (!/[0-9]|[A-F]/i.test(val)) {
			        validaterror.innerHTML = 'Please enter an hex digit (0-9 or A-F).';
					this.classList.add("bg-danger");
					this.classList.add("text-white");
			        return false;
			    }
			    validaterror.innerHTML = '';
			    this.classList.remove("bg-danger");
			    this.classList.remove("text-white");
			}
			
			
		});
		txtx_container.addEventListener("click", function(event) {
		  console.log("click", this, this.oldvalue);
		  this.select();
		});
		txtx_container.addEventListener("blur", function(event) {
		  console.log("blur", this, this.oldvalue);
		  //this.select();
		});
		txtx_container.addEventListener("mouseup", function(event) {
		  console.log("mouseup", this.oldvalue);
		  //return false;
		});
		txtx_container.addEventListener("focusin", function(event) {
		  console.log("focus in event", event.relatedTarget, this.oldvalue);
		  //if (!event.relatedTarget) return false;
		});
		txtx_container.addEventListener("focus", function(event) {
		  event.preventDefault();
		  console.debug("infocus", event.relatedTarget);
		  if (!event.relatedTarget) {
			console.debug("zobi", this);
			//this.select();
			//return ;
		  }
		  this.oldvalue = this.value; //You already have the element as a variable
		  console.log("focus", this.value.length, this.oldvalue, this.selectionStart);
		  //return false;
		  this.select();
		  //return true;
		});
		txtx_container.addEventListener("change", function(event) {
			var validaterror = document.getElementById(typD+'-errorvalidate');
		  console.log("change", this.oldvalue, this.value );
	  if (!/[0-9]|[A-F]/i.test(this.value)) {
	      validaterror.innerHTML = 'Please enter an hex digit (0-9 or A-F).';
		  this.classList.add("bg-danger");
	      this.classList.add("text-white");
		  }
	  else {
		validaterror.innerHTML = '';
		this.classList.remove("bg-danger");
		this.classList.remove("text-white");

		const c1 = super_mycmds[typD];
		const c2 = (Number("0x"+this.value)&0x0F) + ((i<<4)&0xF0);
		const c3 = 0;

		const b1 = new Uint8Array([89, 81, c1, c2, c3]);
		console.debug(b1);
		sendmsg_onclick(b1);
		stored_items[typD][i] = (Number("0x"+this.value)&0x0F);
		localStorage.setItem("stored_"+typD, JSON.stringify(stored_items[typD]));
		console.log("chg",  typD, stored_items[typD]);
	    console.log("chg2", typD, JSON.parse(localStorage.stored_dsplA));
	  }
		});
	}
}

function setInitVals(typD, initVal) {
	const displays = super_gb[typD];

	if (displays) {
		for (let i=0; i< displays.element.length; i++) {
			displays.element[i].container.value = initVal;
		    stored_items[typD][i] = (Number("0x"+initVal)&0x0F);
			localStorage.setItem("stored_"+typD, JSON.stringify(stored_items[typD]));
			}
		}
}
function setDspls(typD) {
	const displays = super_gb[typD];
	
	if (displays) {
		console.debug(displays.element);
		for (let i=0; i< displays.element.length; i++) {
			let ivalue = displays.element[i].container.value;
			console.debug(i, ivalue);
			//YQxyz 
			const c1 = super_mycmds[typD];
			const c2 = (Number("0x"+ivalue)&0x0F) + ((i<<4)&0xF0);
			const c3 = 0;
			
			const b1 = new Uint8Array([89, 81, c1, c2, c3]);
			console.debug(b1);
			sendmsg_onclick(b1);
		}

	}
}
async function start_supervis( ) {

	var checkResetResp;
	for (var i=0; i<5; i++) {
		try {	
			//"YCXQ0"
			checkResetResp = await myRequest(new Uint8Array([89, 67, 88, 81, 48]), "ResetReceived");
			//console.log(checkFletcher, "type",typeof checkFletcher);
			console.log("supervis resolv", checkResetResp);
		}
		catch(err) {
			update_rconsole(`Communication error. Abort<br>`);
			modalShow("Supervision mode unreachable", "Failure. No sync", "bg-danger");
			return;
			
		}
		if (supervisionState != "Supervision is ON") {
			if (checkResetResp[1] == 0x84) {
				console.log("locked in supervisor");
				displayToast("Supervision", "Supervision activated");
				return;
			}
		}
		else {
			if (checkResetResp[1] != 0x84) {
				console.log("exited supervisor");
				displayToast("Supervision", "Supervision stopped");
				return;
			}
			
		}
		await sleep(200);
	
	}
	update_rconsole(`Supervision mode cannot be set. Abort<br>`);
	modalShow("Supervision mode unreachable", "Supervision mode unreachable after 5 attempts.", "bg-danger");
	return;
}
