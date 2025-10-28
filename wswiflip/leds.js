




const gpiotooltip = [
    "C/#F",  //#0     group 3-1
    "C/#E",  //#1     group 3-2
    "C/#D",  //#2     group 3-4
    "C/#C",  //#3     group 3-8
    
    "C/#B",  //#4     group 4-1
    "C/#A",  //#5     group 4-2
    "C/#9",  //#6     group 4-4
    "C/#8",  //#7     group 4-8
    
    "C/#7",  //#8     group 5-1
    "C/#6 (knocker)", // #9     group 5-2
    "NC",    //#10     group 5-4
    "Sound-100K",    //#11     group 5-8
    
    "Sound-10K",     //#12     group 6-1
    "Sound-1K",      //#13     group 6-2
    "Sound-100",     //#14     group 6-4
    "Sound-10",      //#15     group 6-8
    
    "L/61 (bonus)",  //#16    group 7-1
    "L/62 (bonus)",  //#17    group 7-2
    "L/64 (bonus)",  //#18    group 7-4
    "L/68 (bonus)",  //#19    group 7-8
    
    "L/71",   //#20    group 8-1
    "L/72",   //#21    group 8-2
    "L/74",   //#22    group 8-4
    "PLAY SIGNAL"   //#23    group 8-8
    
    ];

const b2tooltip = [
	    "L/51",   //#IO-0
	    "L/52",   //#IO-1
	    "L/54",   //#IO-2
	    "L/58",   //#IO-3
	    "L/41",   //#IO-4
	    "L/42",   //#IO-5
	    "L/44",   //#IO-6
	    "L/48",   //#IO-7
	    "L/31",   //#IO-8
	    "L/32",   //#IO-9
	    "L/34",   //#IO-10
	    "L/38",   //#IO-11
	    "L/21",   //#IO-12
	    "L/22",   //#IO-13
	    "L/24",   //#IO-14
	    "L/28"   //#IO-15
	    ];

		
		
//for the wsc3c.html
const patooltip = [
	"A0",
	"A1",
	"A2",
	"A3",
	"A4",
	"A5",
	"A6",
	"A7"
	];
const pbtooltip = [
		"Money Cntr Signal",
		"B1",
		"Playcntr Signal",
		"Toggle Signal",
		"Turntable MTR Signal",
		"Transfer MTR Signal",
		"Magazine MTR Signal",
		"Detent Signal"
		];
const pctooltip = [
		"C0",
		"C1",
		"C2",
		"C3",
		"C4",
		"C5",
		"C6",
		"C7"
		];
const pdtooltip = [
		"D0",
		"D1",
		"D2",
		"D3",
		"D4",
		"D5",
		"D6",
		"D7"
		];
	
function create_ledbar(ledblock, container_id) {
	const ledcElement = document.getElementById(container_id);
	var   strsgn;
//	const att_ledc = document.createAttribute("class");
//	att_ledc.value = "container overflow-scroll";
//	ledcElement.setAttributeNode(att_ledc);

	if (ledblock == gpiotooltip)
		strsgn = "gpiotooltip";
	else if (ledblock == b2tooltip)
		strsgn = "b2tooltip";
	else
		strsgn = "unknowntooltip";
	
	ledblock.forEach(initleds);
	function initleds(n, index) {
		// Create element:
		const led_container = document.createElement("div");
		ledcElement.appendChild(led_container);
		const att_container = document.createAttribute("class");
		att_container.value = "d-flex flex-column";
		led_container.setAttributeNode(att_container);
		
		
		const led_led = document.createElement("div");
		const led_lbl = document.createElement("div");
	    
		led_lbl.innerText = n;

		// Append to led_container:
		led_container.appendChild(led_lbl);
		led_container.appendChild(led_led);
		
		
		// Create a class attribute:
		const att = document.createAttribute("class");

		// Set the value of the class attribute
		att.value = "led led-black border border-3";

		// Add the class attribute
		led_led.setAttributeNode(att);
		// Create a class attribute:
		const att2 = document.createAttribute("class");
		led_led.setAttribute("id", n+container_id);
		//console.log("ledclass_"+n+container_id);
		//led_led.classList.add("ledclass_"+strsgn+index);
		led_led.setAttribute("title", n);
		led_led.setAttribute("data-bs-toggle", "tooltip");

		// Set the value of the class attribute
		att2.value = "lbl small text-nowrap";//  border border-3";

		// Add the class attribute
		led_lbl.setAttributeNode(att2);
		}
	
}
function create_game_select(container_id) {
	const selectElem = document.getElementById(container_id);

	for (let m in RscModelsArr){
	    var opt = document.createElement('option');
	    opt.value = RscModelsArr[m].name;
	    opt.innerHTML = RscModelsArr[m].name;
	    selectElem.appendChild(opt);
	}	
}

function update_sm_labels_turned(game_select) {
	try {
		var cur_game = game_select.options[ game_select.selectedIndex ].value;
		}
	catch(err) {
		return;
	}
	
    //console.log("cur_game", cur_game);
	for (let row=0; row<4; row++) {
		for (let col=0; col<10; col++) {
			let idx = col+(10*row);
			let lbl_object = document.getElementById("lb-"+idx);
			lbl_object.innerHTML = RscModelsArr[game_select.selectedIndex].content["Switches short"][col][row];
			
		}
	}	
}

function update_sm_labels(game_select) {
	try {
		var cur_game = game_select.options[ game_select.selectedIndex ].value;
		}
	catch(err) {
		return;
	}
	
    //console.log("cur_game", cur_game);
	for (let row=0; row<10; row++) {
		for (let col=0; col<4; col++) {
			let idx = row+(10*col);
			let lbl_object = document.getElementById("lb-"+idx);
			lbl_object.innerHTML = RscModelsArr[game_select.selectedIndex].content["Switches short"][row][col];
			
		}
	}	
}


function create_switch_matrix(container_id) {
	const rlbl = ["A", "B", "C", "D"];
	const ledcElement = document.getElementById(container_id);

//	var yourSelect = document.getElementById( game_select_id );
//	console.log(yourSelect, yourSelect.selectedIndex);
//	var cur_game = yourSelect.options[ yourSelect.selectedIndex ].value;
	
	for (let row=0; row<4; row++) {
		var led_row_container = document.createElement("div");
		led_row_container.setAttribute("class", "row mt-3");
		ledcElement.appendChild(led_row_container);
		
		var header_row_container = document.createElement("div");
		header_row_container.setAttribute("class", "col-1");
		led_row_container.appendChild(header_row_container);
		var header_row_span = document.createElement("span");
		header_row_span.setAttribute("class", "fs-6 d-flex justify-content-center overflow-hidden border");
		header_row_span.innerHTML = rlbl[row];
		header_row_container.appendChild(header_row_span);
		
		for (let col=0; col<10; col++) {
			let idx = col+(10*row);
			var col_led = document.createElement("div");
			col_led.setAttribute("class", "col-1");
			led_row_container.appendChild(col_led);

			var led_object = document.createElement("div");
			led_object.setAttribute("class", "cled led-black border");
			led_object.setAttribute("id", "sm-"+idx);

			var lbl_object = document.createElement("div");
			lbl_object.setAttribute("class", "d-flex justify-content-center overflow-visible small");
			lbl_object.setAttribute("id", "lb-"+idx);
			//console.log(RscModels['Fair Fight']["Switches short"])
			//lbl_object.innerHTML = RscModels['Alaska']["Switches short"][col][row];
			lbl_object.innerHTML = RscModelsArr[0]['content']["Switches short"][col][row];
			
			var led_wrapper = document.createElement("div");
			led_wrapper.setAttribute("class", "d-flex justify-content-center");

			led_wrapper.appendChild(led_object);
			col_led.appendChild(led_wrapper);
			col_led.appendChild(lbl_object);
			
			//<div class="col-1 "><div ><div class="d-flex justify-content-center" ><div class="cled led-green"></div></div><div  class="d-flex justify-content-center overflow-visible small" >Replay.</div></div></div>
            
			
			const b1 = new Uint8Array([89, 83, col, (1<<row), 50]);
			const b2 = new Uint8Array([89, 83, col, (1<<row), 255]);

			led_object.onclick = function() { sendmsg_onclick(b1); };
			led_object.ondblclick = function() { sendmsg_onclick(b2); };
//			//led_led.ondblclick = function() { sendmsg_onclick('YS'+col+(1<<row)+127); };
//			//led_led.onclick = function() { sendmsg_onclick(new Uint8Array([131, 123, col, (1<<row), 50])); };

		}
	}
	
	
}

function create_switch_matrix_ortho(container_id) {
	const rlbl = ["A", "B", "C", "D"];
	const ledcElement = document.getElementById(container_id);

//	var yourSelect = document.getElementById( game_select_id );
//	console.log(yourSelect, yourSelect.selectedIndex);
//	var cur_game = yourSelect.options[ yourSelect.selectedIndex ].value;
	
	for (let row=0; row<10; row++) {
		var led_row_container = document.createElement("div");
		led_row_container.setAttribute("class", "row mt-3");
		ledcElement.appendChild(led_row_container);
		
		var header_row_container = document.createElement("div");
		header_row_container.setAttribute("class", "col-2");
		led_row_container.appendChild(header_row_container);
		var header_row_span = document.createElement("span");
		header_row_span.setAttribute("class", "fs-6 d-flex justify-content-center overflow-hidden border");
		header_row_span.innerHTML = row;
		header_row_container.appendChild(header_row_span);
		
		for (let col=3; col>=0; col--) {
			let idx = row+(10*(col));
			var col_led = document.createElement("div");
			col_led.setAttribute("class", "col-2");
			led_row_container.appendChild(col_led);

			var led_object = document.createElement("div");
			led_object.setAttribute("class", "cled led-black border");
			led_object.setAttribute("id", "sm-"+idx);

			var lbl_object = document.createElement("div");
			lbl_object.setAttribute("class", "d-flex justify-content-center overflow-visible small");
			lbl_object.setAttribute("id", "lb-"+idx);
			//console.log(RscModels['Fair Fight']["Switches short"])
			//lbl_object.innerHTML = RscModels['Alaska']["Switches short"][col][row];
			lbl_object.innerHTML = RscModelsArr[0]['content']["Switches short"][row][(col)];
			//lbl_object.innerHTML = row.toString()+ " "+col.toString();
			
			var led_wrapper = document.createElement("div");
			led_wrapper.setAttribute("class", "d-flex justify-content-center");

			led_wrapper.appendChild(led_object);
			col_led.appendChild(led_wrapper);
			col_led.appendChild(lbl_object);
			
			//<div class="col-1 "><div ><div class="d-flex justify-content-center" ><div class="cled led-green"></div></div><div  class="d-flex justify-content-center overflow-visible small" >Replay.</div></div></div>
            
			
			const b1 = new Uint8Array([89, 83, row, (1<<col), 50]);
			const b2 = new Uint8Array([89, 83, row, (1<<col), 255]);

			led_object.onclick = function() { sendmsg_onclick(b1); };
			led_object.ondblclick = function() { sendmsg_onclick(b2); };
//			//led_led.ondblclick = function() { sendmsg_onclick('YS'+col+(1<<row)+127); };
//			//led_led.onclick = function() { sendmsg_onclick(new Uint8Array([131, 123, col, (1<<row), 50])); };

		}
	}
	
	
}

const rowe_sw_tooltip = [
	["Prem Ratio\n1", "Prem Ratio\n2", "Prem Ratio\n4", "Prem Ratio\n8", "Dollar Bill Bonus 1", "0/5", "Cancel Signal", "+8 on (service switch)"],
    ["1 Play Price 1", "1 Play Price 2", "1 Play Price 4", "1 Play Price 8", "Dollar Bill Bonus 2", "1/5", "STD/As Selected", "Test Switch"],
	["Price of Crd Lvl 1 5c", "Price of Crd Lvl 1 10c", "Price of Crd Lvl 1 20c", "Price of Crd Lvl 1 40c", "Coin Ratio", "2/5", "Manual Credit", "Clear Selection Memory"],
	["Card Level 1 1", "Card Level 1 2", "Card Level 1 4", "Card Level 1 8", "1,2,4,8", "3/5", "Most/Least Popular", "3/7"],
	["Card Level 2 1", "Card Level 2 2", "Card Level 2 4", "Card Level 2 8", "1,2,5,10", "1,2,3,5", "Memorec Advance", "Memorec Reset"],
	["Card Level 3 1", "Card Level 3 2", "Card Level 3 4", "Card Level 3 8", "16 Play Adder", "5/5", "Playmaker Timer", "5/7"],
	["Card Level 4 1", "Card Level 4 2", "Card Level 4 4", "Card Level 4 8", "Outer Cam Switch", "Inner Cam Switch", "Optical Home", "Optical Index"],
	["RESET", "POPULAR", "160 Play", "5c Coin Switch", "10c Coin Switch", "25c Coin Switch", "50c Coin Switch", "$1 Bill Switch"],
	["1", "2", "3", "4", "5", "RI-3", "8/6", "8/7"],
    ["6", "7", "8", "9", "0", "Premium Price Key", "9/6", "9/7"]
];
const rowe_sw_lbl = [
	["PR1", "PR2", "PR4", "PR8", "$B1", "0/5", "Cancel", "+8on"],
	["1PP1", "1PP2", "1PP4", "1PP8", "$B2", "1/5", "S107", "S106"],
	["Crd1 5c", "Crd1 10c", "Crd1 20c", "Crd1 40c", "C. R.", "2/5", "S105", "S104"],
	["Card1 1", "Card1 2", "Card1 4", "Card1 8", "1,2,4,8", "3/5", "S100", "3/7"],
	["Card2 1", "Card2 2", "Card2 4", "Card2 8", "1,2,5,10", "1,2,3,5", "S102", "S101"],
	["Card3 1", "Card3 2", "Card3 4", "Card3 8", "16P+", "5/5", "Play Timer", "5/7"],
	["Card4 1", "Card4 2", "Card4 4", "Card4 8", "O. Cam", "I. Cam", "Optic Home", "Optic Index"],
	["RESET", "POP", "160 P", "5c Sw", "10c Sw", "25c Sw", "50c Sw", "$1 Sw"],
	["1", "2", "3", "4", "5", "RI-3", "8/6", "8/7"],
	["6", "7", "8", "9", "0", "Prem. K.", "9/6", "9/7"]

];
function create_rowe_switch_matrix(container_id) {
	const rlbl = ["A", "B", "C", "D"];
	const ledcElement = document.getElementById(container_id);

//	var yourSelect = document.getElementById( game_select_id );
//	console.log(yourSelect, yourSelect.selectedIndex);
//	var cur_game = yourSelect.options[ yourSelect.selectedIndex ].value;
	
	for (let row=0; row<10; row++) {
		var led_row_container = document.createElement("div");
		led_row_container.setAttribute("class", "row mt-3");
		ledcElement.appendChild(led_row_container);
		
		var header_row_container = document.createElement("div");
		header_row_container.setAttribute("class", "col-1");
		led_row_container.appendChild(header_row_container);
		var header_row_span = document.createElement("span");
		header_row_span.setAttribute("class", "fs-6 d-flex justify-content-center overflow-hidden border");
		header_row_span.innerHTML = row;
		header_row_container.appendChild(header_row_span);
		
		for (let col=0; col<8; col++) {
			let idx = row+(10*(col));
			var col_led = document.createElement("div");
			col_led.setAttribute("class", "col-1");
			led_row_container.appendChild(col_led);

			var led_object = document.createElement("div");
			led_object.setAttribute("class", "cled led-black border");
			led_object.setAttribute("id", "sm-"+idx);
			led_object.setAttribute("data-bs-toggle", "tooltip");
			led_object.title = rowe_sw_tooltip[row][col];

			var lbl_object = document.createElement("div");
			lbl_object.setAttribute("class", "d-flex justify-content-center overflow-visible small");
			lbl_object.setAttribute("id", "lb-"+idx);
			//console.log(RscModels['Fair Fight']["Switches short"])
			//lbl_object.innerHTML = RscModels['Alaska']["Switches short"][col][row];
			
			//lbl_object.innerHTML = RscModelsArr[0]['content']["Switches short"][row][(col)];
			
			lbl_object.innerHTML = row+", "+col;
			//lbl_object.innerHTML = row.toString()+ " "+col.toString();
			lbl_object.innerHTML = rowe_sw_lbl[row][col];
			lbl_object.title = rowe_sw_tooltip[row][col];
			//lbl_object.setAttribute("data-bs-toggle", "tooltip");
			
			var led_wrapper = document.createElement("div");
			led_wrapper.setAttribute("class", "d-flex justify-content-center");

			led_wrapper.appendChild(led_object);
			col_led.appendChild(led_wrapper);
			col_led.appendChild(lbl_object);
			
			//<div class="col-1 "><div ><div class="d-flex justify-content-center" ><div class="cled led-green"></div></div><div  class="d-flex justify-content-center overflow-visible small" >Replay.</div></div></div>
            
			
			const b1 = new Uint8Array([89, 83, row, (1<<col), 50]);
			const b2 = new Uint8Array([89, 83, row, (1<<col), 255]);

			led_object.onclick = function() { console.log(b1); sendmsg_onclick(b1); };
			led_object.ondblclick = function() { console.log(b2); sendmsg_onclick(b2); };
//			//led_led.ondblclick = function() { sendmsg_onclick('YS'+col+(1<<row)+127); };
//			//led_led.onclick = function() { sendmsg_onclick(new Uint8Array([131, 123, col, (1<<row), 50])); };

		}
	}
	
	
}