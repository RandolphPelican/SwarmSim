const canvas = document.getElementById("agentCanvas");
const ctx = canvas.getContext("2d");

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = 350;
}
resize();
window.onresize = resize;

class Agent {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.dx = (Math.random() - 0.5) * 1.2;
        this.dy = (Math.random() - 0.5) * 1.2;
        this.size = 6;
        this.color = ["#ffcc33", "#66ccff", "#ff6699"][Math.floor(Math.random()*3)];
    }

    move() {
        this.x += this.dx;
        this.y += this.dy;

        if (this.x < 0 || this.x > canvas.width) this.dx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.dy *= -1;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI*2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

let agents = [];
for (let i = 0; i < 18; i++) agents.push(new Agent());

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    agents.forEach(a => { a.move(); a.draw(); });
    requestAnimationFrame(animate);
}
animate();
