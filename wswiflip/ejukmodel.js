//this file for simulating the mechanism with vhdl emulator
//get the disc number and triggers on event turntable motor+ outer cam on
//send cancel at the end of the play



const songlist = ["The Residents - Comercial Album - 11 - floyd.mp3",
	"03 picnic boy.mp3",
	"The Residents - Comercial Album - 43 - theme for an american TV Show.mp3",
	"27 birds in the trees.mp3",
	"tautira.mp3",
	"49 this is a mans mans mans world.mp3",
	"50 hit the road jack.mp3",
	"The Residents - Comercial Album - 01 - eastern woman.mp3",
	"The Residents - Comercial Album - 02 - perfect love.mp3",
	"The Residents - Comercial Album - 03 - picnic boy.mp3",
	"The Residents - Comercial Album - 04 - end of home.mp3",
	"The Residents - Comercial Album - 05 - amber.mp3",
	"The Residents - Comercial Album - 07 - secrets.mp3",
	"The Residents - Comercial Album - 08 - die in terror.mp3",
	"The Residents - Comercial Album - 09 - red rider.mp3",
	"The Residents - Comercial Album - 10 - my second wife.mp3",
	"The Residents - Comercial Album - 11 - floyd.mp3",
	"The Residents - Comercial Album - 12 - suburban bathers.mp3",
	"The Residents - Comercial Album - 13 - dimples and toes.mp3",
	"The Residents - Comercial Album - 14 - the nameles souls.mp3",
	"The Residents - Comercial Album - 15 - love leaks out.mp3",
	"The Residents - Comercial Album - 16 - act of being polite.mp3",
	"The Residents - Comercial Album - 17 - medicine man.mp3",
	"The Residents - Comercial Album - 18 - tragic bells.mp3",
	"The Residents - Comercial Album - 20 - the simple song.mp3",
	"The Residents - Comercial Album - 21 - ups and downs.mp3",
	"The Residents - Comercial Album - 22 - possessions.mp3",
	"The Residents - Comercial Album - 23 - give it to someone else.mp3",
	"The Residents - Comercial Album - 24 - phantom.mp3",
	"The Residents - Comercial Album - 25 - less not more.mp3",
	"The Residents - Comercial Album - 26 - my work is so behind.mp3",
	"The Residents - Comercial Album - 27 - birds in the trees.mp3",
	"The Residents - Comercial Album - 28 - handfull of desire.mp3",
	"The Residents - Comercial Album - 29 - moisture.mp3",
	"The Residents - Comercial Album - 30 - love is.mp3",
	"The Residents - Comercial Album - 31 - troubled man.mp3",
	"The Residents - Comercial Album - 32 - LA LA.mp3",
	"The Residents - Comercial Album - 33 - loneliness.mp3",
	"The Residents - Comercial Album - 34 - nice old man.mp3",
	"The Residents - Comercial Album - 36 - fingertrips.mp3",
	"The Residents - Comercial Album - 37 - in betwinen dreams.mp3",
	"The Residents - Comercial Album - 38 - margaret freeman.mp3",
	"The Residents - Comercial Album - 39 - the comming of the crow.mp3",
	"The Residents - Comercial Album - 40 - when we were young.mp3",
	"The Residents - Comercial Album - 41 - shut up shut up.mp3",
	"The Residents - Comercial Album - 42 - and i was alone.mp3",
	"The Residents - Comercial Album - 43 - theme for an american TV Show.mp3",
	"Cleaning Out My Close.mp3",
	"graeme allwright - Prison song.mp3",
	"Nada surf - L'aventurier (Indochine.mp3",
	"Nique La Police.mp3",
	"The Residents - Comercial Album - 44 - were a happy family.mp3",
	"03 picnic boy.mp3",
	"The Residents - Comercial Album - 43 - theme for an american TV Show.mp3",
	"27 birds in the trees.mp3",
	"tautira.mp3",
	"49 this is a mans mans mans world.mp3",
	"50 hit the road jack.mp3",
	"The Residents - Comercial Album - 01 - eastern woman.mp3",
	"The Residents - Comercial Album - 02 - perfect love.mp3",
	"The Residents - Comercial Album - 03 - picnic boy.mp3",
	"The Residents - Comercial Album - 04 - end of home.mp3",
	"The Residents - Comercial Album - 05 - amber.mp3",
	"The Residents - Comercial Album - 07 - secrets.mp3",
	"The Residents - Comercial Album - 08 - die in terror.mp3",
	"The Residents - Comercial Album - 09 - red rider.mp3",
	"The Residents - Comercial Album - 10 - my second wife.mp3",
	"The Residents - Comercial Album - 11 - floyd.mp3",
	"The Residents - Comercial Album - 12 - suburban bathers.mp3",
	"The Residents - Comercial Album - 13 - dimples and toes.mp3",
	"The Residents - Comercial Album - 14 - the nameles souls.mp3",
	"The Residents - Comercial Album - 15 - love leaks out.mp3",
	"The Residents - Comercial Album - 16 - act of being polite.mp3",
	"The Residents - Comercial Album - 17 - medicine man.mp3",
	"The Residents - Comercial Album - 18 - tragic bells.mp3",
	"The Residents - Comercial Album - 20 - the simple song.mp3",
	"The Residents - Comercial Album - 21 - ups and downs.mp3",
	"The Residents - Comercial Album - 22 - possessions.mp3",
	"The Residents - Comercial Album - 23 - give it to someone else.mp3",
	"The Residents - Comercial Album - 24 - phantom.mp3",
	"The Residents - Comercial Album - 25 - less not more.mp3",
	"The Residents - Comercial Album - 26 - my work is so behind.mp3",
	"The Residents - Comercial Album - 27 - birds in the trees.mp3",
	"The Residents - Comercial Album - 28 - handfull of desire.mp3",
	"The Residents - Comercial Album - 29 - moisture.mp3",
	"The Residents - Comercial Album - 30 - love is.mp3",
	"The Residents - Comercial Album - 31 - troubled man.mp3",
	"The Residents - Comercial Album - 32 - LA LA.mp3",
	"The Residents - Comercial Album - 33 - loneliness.mp3",
	"The Residents - Comercial Album - 34 - nice old man.mp3",
	"The Residents - Comercial Album - 36 - fingertrips.mp3",
	"The Residents - Comercial Album - 37 - in betwinen dreams.mp3",
	"The Residents - Comercial Album - 38 - margaret freeman.mp3",
	"The Residents - Comercial Album - 39 - the comming of the crow.mp3",
	"The Residents - Comercial Album - 40 - when we were young.mp3",
	"The Residents - Comercial Album - 41 - shut up shut up.mp3",
	"The Residents - Comercial Album - 42 - and i was alone.mp3",
	"The Residents - Comercial Album - 43 - theme for an american TV Show.mp3",
	"Cleaning Out My Close.mp3",
	"graeme allwright - Prison song.mp3",
	"Nada surf - L'aventurier (Indochine.mp3",
	"Nique La Police.mp3"	
	
];

var vjukOn = false;

var t_mt;
var mag_counter = 0;
var trsf_counter = 0;
var jk_discnum;
var jk_transfer_state;
 
var status_0 = false;
var status_1 = false;
var init_t_pos = "rest";

var cur_audio;

const obs = new MutationObserver(() => {
	const el = document.getElementById('sm-60');
  if (el.classList.contains('led-yellow')) {
	try {
		cur_audio.pause();
		cur_audio.currentTime = 0; // optional: reset to start = 
	    //console.log('led-yellow class added');
		}
	catch(err)
	{}
  } else {
    //console.log('led-yellow class removed');
  }
});
// later: obs.disconnect();

async function playAudio(url) {
  const b0 = new Uint8Array([89, 83, 0, (1<<6), 5]); //cancel switch
  const el = document.getElementById('sm-60');
  const elfile = document.getElementById('jk-file-playing');

  let songFace = document.getElementById("Z402").textContent;

  let songNum = ejk_disc_num;
  
  const url2 = url+songlist[Number(songNum)];
  cur_audio = new Audio(url2);
  elfile.innerHTML = songlist[Number(songNum)];
  
  obs.observe(el, { attributes: true, attributeFilter: ['class'] });

  console.log("song num", songFace, songNum, url2, el);
  cur_audio.addEventListener("ended", () => {
	sendmsg_onclick(b0);
    console.log("end", b0);
	elfile.innerHTML = "";
  });
  await cur_audio.play(); // resolves when playback starts (or rejects on error)
  return cur_audio;       // keep a handle if you want pause/stop later
}

function create_ejuke() {
	
	t_mt = setInterval(magazineTimer, 250);
	
	console.log("songlist size:", songlist.length);
	console.log("cur url", window.location.href);
	
	}

var lastsm46state = false;	
function magazineTimer() {
	let PB6Elem = document.getElementById(pbtooltip[6]+"pb-bar"); // PB6<=>  MagazineMtr signal
	let PB5Elem = document.getElementById(pbtooltip[5]+"pb-bar"); // PB5<=>  TransferMtr signal
	let PB4Elem = document.getElementById(pbtooltip[4]+"pb-bar"); // PB4<=>  Turntable signal
	const b0 = new Uint8Array([89, 83, 6, (1<<6), 255]);
	const b3 = new Uint8Array([89, 83, 6, (1<<6), 1]);
	const b1 = new Uint8Array([89, 83, 6, (1<<7), 1]);
	const b2 = new Uint8Array([89, 83, 6, (1<<7), 255]);
	
	const b65_on  = new Uint8Array([89, 83, 6, (1<<5), 255]);
	const b65_off = new Uint8Array([89, 83, 6, (1<<5), 1]);
	const b64_on  = new Uint8Array([89, 83, 6, (1<<4), 255]);
	const b64_off = new Uint8Array([89, 83, 6, (1<<4), 1]);


	if (vjukOn==false) return;
	 
		//turntable is turning
		const el = document.getElementById('sm-46');  //outer cam

		if (el.classList.contains("led-yellow")===true && lastsm46state==false) {
			if (PB4Elem.classList.contains("led-black")===true) {
			
				console.log("lets start a disc");
				if (window.location.href.startsWith('file://'))
					playAudio('file:///Users/garzol/git/wswiflip/wswiflip/music/');
				else
					playAudio('http://aa55.fr/wswiflip/music/');
			}
		
		}
		lastsm46state = el.classList.contains("led-yellow");
}