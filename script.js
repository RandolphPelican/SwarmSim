/* landing/script.js
   Final demo engine (Style A). Demo-mode animation for <=10 agents.
   Data/research mode disables heavy drawing for >10 agents.
*/

(() => {
  // elements
  const canvas = document.getElementById('simCanvas');
  const ctx = canvas.getContext('2d');
  const agentCountInput = document.getElementById('agentCount');
  const pGreedy = document.getElementById('pGreedy');
  const pCautious = document.getElementById('pCautious');
  const pExplorer = document.getElementById('pExplorer');
  const foodCountInput = document.getElementById('foodCount');
  const dangerCountInput = document.getElementById('dangerCount');
  const spawnBtn = document.getElementById('spawnBtn');
  const startBtn = document.getElementById('startBtn');
  const pauseBtn = document.getElementById('pauseBtn');

  const modeLabel = document.getElementById('modeLabel');
  const tickLabel = document.getElementById('tick');
  const statAgents = document.getElementById('statAgents');
  const statFood = document.getElementById('statFood');
  const statDanger = document.getElementById('statDanger');
  const statScore = document.getElementById('statScore');

  // canvas sizing
  function resize() {
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * devicePixelRatio;
    canvas.height = rect.height * devicePixelRatio;
    ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);
  }
  // set initial CSS size if not set
  if (!canvas.style.width) canvas.style.width = '100%';
  if (!canvas.style.height) canvas.style.height = '360px';

  window.addEventListener('resize', resize);
  resize();

  // state
  let agents = [], foods = [], dangers = [];
  let running = false, tick = 0, score = 0, raf = null;

  // util
  const rand = (min,max) => Math.random()*(max-min)+min;
  const clamp = (v,a,b) => Math.max(a, Math.min(b, v));
  function dist(a,b){ const dx=a.x-b.x, dy=a.y-b.y; return Math.hypot(dx,dy); }

  // visual configs
  const AGENT_CFG = {
    greedy: {color:'#ff6b6b', r:10},
    cautious: {color:'#60a5fa', r:10},
    explorer: {color:'#ffd166', r:10}
  };

  // spawn helpers
  function newAgent(type){
    return {
      x: rand(40, canvas.width/devicePixelRatio - 40),
      y: rand(40, canvas.height/devicePixelRatio - 40),
      vx: rand(-0.8,0.8),
      vy: rand(-0.8,0.8),
      type, wobble: Math.random()*10, score:0
    };
  }
  function spawnAll(){
    agents = []; foods = []; dangers = []; tick=0; score=0;
    let N = Math.max(1, Math.floor(Number(agentCountInput.value) || 5));
    const gp = Number(pGreedy.value)||0, cp = Number(pCautious.value)||0, ep = Number(pExplorer.value)||0;
    const total = (gp+cp+ep) || 100;
    const g = Math.round((gp/total)*N), c = Math.round((cp/total)*N), e = Math.max(0, N-g-c);
    for(let i=0;i<g;i++) agents.push(newAgent('greedy'));
    for(let i=0;i<c;i++) agents.push(newAgent('cautious'));
    for(let i=0;i<e;i++) agents.push(newAgent('explorer'));

    const foodN = Math.max(0, Math.floor(Number(foodCountInput.value)||9));
    for(let i=0;i<foodN;i++){
      const val = (i%3===0?10:(i%3===1?6:2));
      foods.push({ x:rand(40, canvas.width/devicePixelRatio-40), y:rand(40, canvas.height/devicePixelRatio-40), value: val, mobile: Math.random()<0.3, vx:rand(-0.5,0.5), vy:rand(-0.5,0.5) });
    }

    const dangerN = Math.max(0, Math.floor(Number(dangerCountInput.value)||5));
    for(let i=0;i<dangerN;i++){
      const sev = (i%3===0?10:(i%3===1?6:2));
      dangers.push({ x:rand(40, canvas.width/devicePixelRatio-40), y:rand(40, canvas.height/devicePixelRatio-40), severity: sev, mobile: Math.random()<0.4, vx:rand(-0.6,0.6), vy:rand(-0.6,0.6) });
    }

    updateStats();
    renderOnce();
  }

  // simple behaviors
  function stepOnce(){
    // move mobile items
    for(const f of foods){ if(f.mobile){ f.x+=f.vx; f.y+=f.vy; if(f.x<20||f.x>canvas.width/devicePixelRatio-20) f.vx*=-1; if(f.y<20||f.y>canvas.height/devicePixelRatio-20) f.vy*=-1; } }
    for(const d of dangers){ if(d.mobile){ d.x+=d.vx; d.y+=d.vy; if(d.x<20||d.x>canvas.width/devicePixelRatio-20) d.vx*=-1; if(d.y<20||d.y>canvas.height/devicePixelRatio-20) d.vy*=-1; } }

    // agent logic
    for(const a of agents){
      if(a.type==='greedy'){
        // seek best food
        let best=null, bestScore=-Infinity;
        for(const f of foods){ const s = f.value - dist(a,f)*0.02; if(s>bestScore){ bestScore=s; best=f; } }
        if(best){ const dx=best.x-a.x, dy=best.y-a.y, m=Math.hypot(dx,dy)||1; a.vx += dx/m * 0.05; a.vy += dy/m * 0.05; }
      } else if(a.type==='cautious'){
        // flee highest danger nearby
        let near=null, nd=Infinity;
        for(const d of dangers){ const dd=dist(a,d); if(dd<nd){ nd=dd; near=d; } }
        if(near && nd<120){ a.vx += (a.x-near.x)*0.003; a.vy += (a.y-near.y)*0.003; }
        // small attraction to food
        if(foods.length){ const any = foods[Math.floor(Math.random()*foods.length)]; a.vx += (any.x-a.x)*0.0008; a.vy += (any.y-a.y)*0.0008; }
      } else {
        // explorer random walk
        a.vx += rand(-0.02,0.02); a.vy += rand(-0.02,0.02);
      }
      // damp and move
      a.vx *= 0.98; a.vy *= 0.98;
      a.x += a.vx; a.y += a.vy;
      // bounds
      a.x = clamp(a.x, 12, canvas.width/devicePixelRatio-12);
      a.y = clamp(a.y, 12, canvas.height/devicePixelRatio-12);

      // interactions
      for(let i=foods.length-1;i>=0;i--){
        if(dist(a, foods[i]) < 14){ score += foods[i].value; a.score = (a.score||0)+foods[i].value; foods.splice(i,1); }
      }
      for(let i=dangers.length-1;i>=0;i--){
        if(dist(a, dangers[i]) < 14){ score -= dangers[i].severity; a.score = (a.score||0)-dangers[i].severity; if(Math.random()<0.06) dangers.splice(i,1); }
      }
    }

    tick++;
    updateStats();
  }

  // drawing
  function drawAgent(a){
    const cfg = AGENT_CFG[a.type] || {color:'#ffd166', r:10};
    ctx.save();
    ctx.translate(a.x, a.y);
    const bob = Math.sin((tick + (a.wobble||0))*0.25) * 2;
    ctx.beginPath();
    const grd = ctx.createRadialGradient(0,bob,1,0,bob,cfg.r*2);
    grd.addColorStop(0, cfg.color);
    grd.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = grd;
    ctx.arc(0, bob, cfg.r, 0, Math.PI*2);
    ctx.fill();
    // inner core
    ctx.beginPath();
    ctx.fillStyle = '#021217';
    ctx.arc(0, bob, cfg.r*0.45, 0, Math.PI*2);
    ctx.fill();
    ctx.restore();
  }

  function drawFood(f){
    ctx.save();
    ctx.translate(f.x, f.y);
    const col = f.value>=8? '#ffd54a' : f.value>=5? '#9ee493' : '#b5e0ff';
    ctx.beginPath(); ctx.fillStyle = col; ctx.arc(0,0,8,0,Math.PI*2); ctx.fill();
    ctx.restore();
  }
  function drawDanger(d){
    ctx.save();
    ctx.translate(d.x, d.y);
    const col = d.severity>=8? '#ff7f50' : d.severity>=5? '#ffb3a7' : '#ffdfd5';
    ctx.beginPath(); ctx.fillStyle = col; ctx.rect(-7,-7,14,14); ctx.fill();
    ctx.restore();
  }

  function render(){
    // clear & subtle background
    ctx.clearRect(0,0,canvas.width,canvas.height);
    // background grid (subtle)
    const w = canvas.width/devicePixelRatio, h = canvas.height/devicePixelRatio;
    ctx.fillStyle = '#031217';
    ctx.fillRect(0,0,w,h);

    // draw food & dangers
    for(const f of foods) drawFood(f);
    for(const d of dangers) drawDanger(d);

    // draw agents
    for(const a of agents) drawAgent(a);
  }

  function renderOnce(){ // single frame render (used after spawn)
    if(agents.length <= 10) render();
    else { /* no heavy render for data mode */ ctx.clearRect(0,0,canvas.width,canvas.height); }
  }

  // loop
  function loop(){
    if(!running) return;
    // do a simulation step
    if(agents.length <= 500){ // lightweight stepping even for larger but not huge
      stepOnce();
    } else {
      // for extremely large sims, perform vectorized steps externally (not here)
      tick += 1;
      updateStats();
    }

    // rendering
    if(agents.length <= 10){
      render();
      raf = requestAnimationFrame(loop);
    } else {
      // data mode: reduce visual work
      if(raf) { cancelAnimationFrame(raf); raf = null; }
      setTimeout(loop, 160); // slower heartbeat for UI updates
    }
  }

  // update UI stats
  function updateStats(){
    modeLabel.textContent = (agents.length <= 10) ? 'demo' : 'data';
    tickLabel.textContent = String(tick);
    statAgents.textContent = String(agents.length);
    statFood.textContent = String(foods.length);
    statDanger.textContent = String(dangers.length);
    statScore.textContent = String(Math.max(0, Math.round(score)));
  }

  // events
  spawnBtn.addEventListener('click', () => { spawnAll(); });
  startBtn.addEventListener('click', () => { if(!running){ running=true; loop(); } });
  pauseBtn.addEventListener('click', () => { running=false; if(raf){ cancelAnimationFrame(raf); raf=null; } });

  // init
  spawnAll();

  // gentle logo spin
  const logo = document.getElementById('logo');
  let logoAng = 0;
  setInterval(()=>{ logoAng = (logoAng + 0.6) % 360; logo.style.transform = `rotate(${logoAng}deg)`; }, 70);
})();
