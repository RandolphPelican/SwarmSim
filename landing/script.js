document.addEventListener("DOMContentLoaded", () => {
  console.log("SwarmSim landing page loaded");

  // Button hover animation
  const buttons = document.querySelectorAll(".btn");
  buttons.forEach(btn => {
    btn.addEventListener("mouseenter", () => {
      btn.style.transform = "scale(1.05)";
      btn.style.transition = "transform 0.2s";
    });
    btn.addEventListener("mouseleave", () => {
      btn.style.transform = "scale(1)";
    });
  });

  // Logo rotation animation
  const logo = document.querySelector(".logo");
  if (logo) {
    let angle = 0;
    setInterval(() => {
      angle = (angle + 0.2) % 360;
      logo.style.transform = `rotate(${angle}deg)`;
    }, 30);
  }

  // Sliders for scenario preview
  const agentCount = document.getElementById("agentCount");
  const agentCountValue = document.getElementById("agentCountValue");
  const bandwidth = document.getElementById("bandwidth");
  const bandwidthValue = document.getElementById("bandwidthValue");

  if (agentCount && agentCountValue) {
    agentCount.addEventListener("input", () => {
      agentCountValue.textContent = agentCount.value;
    });
  }

  if (bandwidth && bandwidthValue) {
    bandwidth.addEventListener("input", () => {
      bandwidthValue.textContent = bandwidth.value;
    });
  }
});
