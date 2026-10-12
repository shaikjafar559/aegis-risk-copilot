/**
 * OmniStory Dynamic Backdrop & Spectrum Visualizer
 * Procedural generative canvas with adaptive themes and audio-reactive animations
 */
class StudioVisualizer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.currentTheme = 'cyber_grid';
    this.activeSpeaker = null; // 'maya', 'leo', 'narrator', null
    this.emotionValence = 'analytical';
    this.energy = 0.5;
    this.time = 0;
    this.particles = [];

    this.resize();
    window.addEventListener('resize', () => this.resize());
    this.initParticles();
    this.animate();
  }

  resize() {
    this.width = this.canvas.parentElement.clientWidth;
    this.height = this.canvas.parentElement.clientHeight;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
  }

  initParticles() {
    this.particles = [];
    for (let i = 0; i < 60; i++) {
      this.particles.push({
        x: Math.random() * (this.width || 800),
        y: Math.random() * (this.height || 450),
        vx: (Math.random() - 0.5) * 1.2,
        vy: (Math.random() - 0.5) * 1.2,
        radius: Math.random() * 2.5 + 1,
        alpha: Math.random() * 0.7 + 0.3
      });
    }
  }

  setTheme(themeName) {
    this.currentTheme = themeName || 'cyber_grid';
  }

  setSpeaker(speaker, emotion) {
    this.activeSpeaker = speaker;
    this.emotionValence = emotion || 'analytical';
    this.energy = speaker ? 1.0 : 0.4;
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    this.time += 0.02;

    // Smooth decay of speaking energy
    if (this.activeSpeaker && this.energy < 0.9) {
      this.energy += 0.05;
    } else if (!this.activeSpeaker && this.energy > 0.4) {
      this.energy -= 0.02;
    }

    this.ctx.clearRect(0, 0, this.width, this.height);

    switch (this.currentTheme) {
      case 'neural_glow':
        this.renderNeuralGlow();
        break;
      case 'quantum_lattice':
        this.renderQuantumLattice();
        break;
      case 'biolum_synth':
        this.renderBiolumSynth();
        break;
      case 'studio_pulse':
      case 'nebula_space':
        this.renderStudioPulse();
        break;
      case 'cyber_grid':
      default:
        this.renderCyberGrid();
        break;
    }

    // Overlay subtle audio reactive spectrum bars at bottom
    this.renderBottomSpectrum();
  }

  renderCyberGrid() {
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;
    const horizon = h * 0.55;

    // Deep dark sky gradient
    const skyGrad = ctx.createLinearGradient(0, 0, 0, horizon);
    skyGrad.addColorStop(0, '#030509');
    skyGrad.addColorStop(1, '#091024');
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, w, horizon);

    // Distant synth sun/orb
    const orbGrad = ctx.createRadialGradient(w / 2, horizon - 10, 5, w / 2, horizon - 10, 90);
    orbGrad.addColorStop(0, 'rgba(0, 240, 255, 0.4)');
    orbGrad.addColorStop(0.5, 'rgba(168, 85, 247, 0.15)');
    orbGrad.addColorStop(1, 'transparent');
    ctx.fillStyle = orbGrad;
    ctx.beginPath();
    ctx.arc(w / 2, horizon - 10, 90, 0, Math.PI * 2);
    ctx.fill();

    // 3D Perspective Grid
    ctx.strokeStyle = `rgba(0, 240, 255, ${0.15 * this.energy + 0.08})`;
    ctx.lineWidth = 1;

    // Horizon line
    ctx.beginPath();
    ctx.moveTo(0, horizon);
    ctx.lineTo(w, horizon);
    ctx.stroke();

    // Vanishing perspective rays
    const fovLines = 26;
    for (let i = 0; i <= fovLines; i++) {
      const bottomX = (w / fovLines) * i;
      ctx.beginPath();
      ctx.moveTo(w / 2, horizon);
      ctx.lineTo(bottomX, h);
      ctx.stroke();
    }

    // Moving horizontal grid lines
    const offset = (this.time * 25) % 30;
    for (let y = horizon; y < h; y += 14) {
      const perspectiveY = horizon + Math.pow((y - horizon) / (h - horizon), 1.8) * (h - horizon) + offset;
      if (perspectiveY <= h && perspectiveY >= horizon) {
        ctx.beginPath();
        ctx.moveTo(0, perspectiveY);
        ctx.lineTo(w, perspectiveY);
        ctx.stroke();
      }
    }
  }

  renderNeuralGlow() {
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;

    // Dark backdrop
    ctx.fillStyle = '#050711';
    ctx.fillRect(0, 0, w, h);

    // Update & draw synaptic particles
    ctx.lineWidth = 0.8;
    for (let i = 0; i < this.particles.length; i++) {
      const p1 = this.particles[i];
      p1.x += p1.vx * (this.energy * 1.2);
      p1.y += p1.vy * (this.energy * 1.2);

      if (p1.x < 0) p1.x = w;
      if (p1.x > w) p1.x = 0;
      if (p1.y < 0) p1.y = h;
      if (p1.y > h) p1.y = 0;

      // Draw particle
      ctx.fillStyle = this.activeSpeaker === 'maya' ? 'rgba(0, 240, 255, 0.8)' : 'rgba(168, 85, 247, 0.8)';
      ctx.beginPath();
      ctx.arc(p1.x, p1.y, p1.radius, 0, Math.PI * 2);
      ctx.fill();

      // Connect nearby particles
      for (let j = i + 1; j < this.particles.length; j++) {
        const p2 = this.particles[j];
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 100) {
          const alpha = (1 - dist / 100) * 0.25 * this.energy;
          ctx.strokeStyle = `rgba(0, 240, 255, ${alpha})`;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
    }
  }

  renderQuantumLattice() {
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;

    ctx.fillStyle = '#060914';
    ctx.fillRect(0, 0, w, h);

    const cols = 28;
    const rows = 14;
    const cellW = w / cols;
    const cellH = h / rows;

    ctx.lineWidth = 1;
    for (let r = 0; r < rows; r++) {
      ctx.beginPath();
      for (let c = 0; c <= cols; c++) {
        const x = c * cellW;
        const wave = Math.sin(c * 0.35 + this.time * 1.8) * Math.cos(r * 0.4 + this.time) * (20 * this.energy);
        const y = r * cellH + wave + 40;
        if (c === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = `rgba(168, 85, 247, ${0.18 + (r / rows) * 0.25 * this.energy})`;
      ctx.stroke();
    }
  }

  renderBiolumSynth() {
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;

    ctx.fillStyle = '#040b0f';
    ctx.fillRect(0, 0, w, h);

    const waves = 4;
    for (let i = 0; i < waves; i++) {
      ctx.beginPath();
      const baseH = h * 0.4 + i * 40;
      ctx.moveTo(0, h);
      ctx.lineTo(0, baseH);

      for (let x = 0; x <= w; x += 15) {
        const waveY = baseH + Math.sin(x * 0.008 + this.time * 1.2 + i * 1.5) * (30 * this.energy) + Math.cos(x * 0.015 - this.time * 0.8) * 15;
        ctx.lineTo(x, waveY);
      }

      ctx.lineTo(w, h);
      ctx.closePath();

      const grad = ctx.createLinearGradient(0, baseH - 40, 0, h);
      grad.addColorStop(0, `rgba(16, 185, 129, ${0.15 * this.energy})`);
      grad.addColorStop(0.5, `rgba(0, 240, 255, ${0.08 * this.energy})`);
      grad.addColorStop(1, 'transparent');
      ctx.fillStyle = grad;
      ctx.fill();
    }
  }

  renderStudioPulse() {
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;

    ctx.fillStyle = '#080816';
    ctx.fillRect(0, 0, w, h);

    const cx = w / 2;
    const cy = h * 0.4;
    const rings = 5;

    for (let r = 1; r <= rings; r++) {
      const radius = (r * 40 + (this.time * 30) % 50) * (this.energy * 0.8 + 0.4);
      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(245, 158, 11, ${Math.max(0, 0.4 - radius / 300)})`;
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
  }

  renderBottomSpectrum() {
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;
    const barCount = 48;
    const barWidth = w / barCount - 2;

    for (let i = 0; i < barCount; i++) {
      const noise = Math.sin(i * 0.5 + this.time * 4) * Math.cos(i * 0.3 - this.time * 3);
      const barHeight = (Math.abs(noise) * 24 + 4) * (this.energy * 1.4);
      const x = i * (barWidth + 2);
      const y = h - barHeight;

      const grad = ctx.createLinearGradient(x, y, x, h);
      grad.addColorStop(0, this.activeSpeaker === 'maya' ? '#00f0ff' : (this.activeSpeaker === 'leo' ? '#a855f7' : '#94a3b8'));
      grad.addColorStop(1, 'transparent');

      ctx.fillStyle = grad;
      ctx.fillRect(x, y, barWidth, barHeight);
    }
  }
}

window.StudioVisualizer = StudioVisualizer;
