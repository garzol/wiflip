


const N = 500; // points max affichés



const start = Date.now();

const trace1 = {
  x: [],
  y: [],
  type: "scatter",
  mode: "lines",
  name: "Optic index"
};

const trace2 = {
  x: [],
  y: [],
  type: "scatter",
  mode: "lines",
  name: "Optic home"
};

const trace3 = {
  x: [],
  y: [],
  type: "scatter",
  mode: "lines",
  name: "Inner cam"
};

const trace4 = {
  x: [],
  y: [],
  type: "scatter",
  mode: "lines",
  name: "Outer cam"
};

const trace5 = {
  x: [],
  y: [],
  type: "scatter",
  mode: "lines",
  name: "PB7 - Detent"
};

const trace6 = {
  x: [],
  y: [],
  type: "scatter",
  mode: "lines",
  name: "PB6 - Magazine motor"
};

const trace7 = {
  x: [],
  y: [],
  type: "scatter",
  mode: "lines",
  name: "PB5 - Transfer motor"
};

const trace8 = {
  x: [],
  y: [],
  type: "scatter",
  mode: "lines",
  name: "PB4 - Turntable motor"
};

const trace9 = {
  x: [],
  y: [],
  type: "scatter",
  mode: "lines",
  name: "PB3 - Toggle"
};

const trace10 = {
  x: [],
  y: [],
  type: "scatter",
  mode: "lines",
  name: "PB2 - Play control"
};

const layout = {
  title: "Signaux tout ou rien",
  xaxis: { title: "Sample" },
  yaxis: { title: "" },
  legend: { orientation: "v" }
};

const config = { responsive: true };

Plotly.newPlot("plot", [trace1, trace2, trace3, trace4, 
	                    trace5, trace6, trace7, trace8,
					    trace9, trace10], layout, config);

setInterval(() => {

	while (chunkportb.length > N)
	    { chunkportb.shift();  }

	while (chunksens.length > N)
	    { chunksens.shift();  }

  const time = chunkportb.map(x => x[0]);
  const pb   = chunkportb.map(x => x[1]);
  const pb7  = chunkportb.map(x => ((x[1]&0x80)>>7)+15);
  const pb6  = chunkportb.map(x => ((x[1]&0x40)>>6)+12);
  const pb5  = chunkportb.map(x => ((x[1]&0x20)>>5)+9);
  const pb4  = chunkportb.map(x => ((x[1]&0x10)>>4)+6);
  const pb3  = chunkportb.map(x => ((x[1]&0x08)>>3)+3);
  const pb2  = chunkportb.map(x => ((x[1]&0x04)>>2));
  //console.log(pb);
  //console.log(pb7);
  
  //Plotly.update('plot', {x: [time], y: [val]});
  
  const tims = chunksens.map(x => x[0]);
  const vals  = chunksens.map(x => x[1]);
  //Plotly.update('plot', {x: [time], y: [pb6]});
  const s6r7 = chunksens.map(x => (x[1]&0x01)+18);
  const s6r6 = chunksens.map(x => ((x[1]&0x02)>>1)+21);
  const s6r5 = chunksens.map(x => ((x[1]&0x04)>>2)+24);
  const s6r4 = chunksens.map(x => ((x[1]&0x08)>>3)+27);
  
  
  
  // trace 0 = première courbe, trace 1 = deuxième courbe
  Plotly.update('plot', {
    x: [tims,tims,tims,tims, time,time,time,time,time,time],
    y: [s6r7,s6r6,s6r5,s6r4, pb7,pb6,pb5,pb4,pb3,pb2],
    'line.color': ['red','green','blue','LightSeaGreen', 'purple', 
		           'crimson', 'black', 'CornflowerBlue', 'Indigo', 'Chartreuse']   // ex: ['#e41a1c','#377eb8']
  });

  //Plotly.update('plot', traces, { legend: {orientation:'h'} });
  
}, 500);
