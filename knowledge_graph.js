/**
 * OmniStory Interactive Knowledge Graph
 * Real-time semantic entity renderer with active-speech illumination and click inspection
 */
class KnowledgeGraphVisualizer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.entities = [];
    this.nodes = [];
    this.edges = [];
    this.activeEntityId = null;
    this.hoveredNode = null;
    this.onSelectEntity = null;

    this.resize();
    window.addEventListener('resize', () => this.resize());
    this.setupListeners();
    this.animate();
  }

  resize() {
    this.width = this.canvas.parentElement.clientWidth;
    this.height = this.canvas.parentElement.clientHeight;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
    this.layoutNodes();
  }

  setData(entities, onSelect) {
    this.entities = entities || [];
    this.onSelectEntity = onSelect;
    this.layoutNodes();
  }

  layoutNodes() {
    const n = this.entities.length;
    if (n === 0) {
      this.nodes = [];
      this.edges = [];
      return;
    }

    const cx = this.width / 2;
    const cy = this.height / 2;
    const radius = Math.min(cx, cy) * 0.65;

    this.nodes = this.entities.map((e, i) => {
      const angle = (i / n) * Math.PI * 2;
      return {
        id: e.id,
        label: e.label,
        category: e.category,
        description: e.description,
        connections: e.connections || [],
        x: cx + Math.cos(angle) * radius,
        y: cy + Math.sin(angle) * radius,
        targetX: cx + Math.cos(angle) * radius,
        targetY: cy + Math.sin(angle) * radius,
        r: 16,
        pulse: 0
      };
    });

    // Build edges
    this.edges = [];
    this.nodes.forEach(source => {
      source.connections.forEach(targetId => {
        const target = this.nodes.find(node => node.id === targetId);
        if (target) {
          this.edges.push({ source, target });
        }
      });
    });
  }

  highlightByTerm(term) {
    if (!term) return;
    const clean = term.toLowerCase();
    const found = this.nodes.find(n => n.label.toLowerCase().includes(clean) || clean.includes(n.label.toLowerCase()));
    if (found) {
      this.activeEntityId = found.id;
      found.pulse = 1.0;
      if (this.onSelectEntity) {
        this.onSelectEntity(found);
      }
    }
  }

  setupListeners() {
    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      let found = null;
      for (const node of this.nodes) {
        const d = Math.hypot(node.x - mx, node.y - my);
        if (d <= node.r + 4) {
          found = node;
          break;
        }
      }
      this.hoveredNode = found;
      this.canvas.style.cursor = found ? 'pointer' : 'default';
    });

    this.canvas.addEventListener('click', (e) => {
      if (this.hoveredNode) {
        this.activeEntityId = this.hoveredNode.id;
        this.hoveredNode.pulse = 1.0;
        if (this.onSelectEntity) {
          this.onSelectEntity(this.hoveredNode);
        }
      }
    });
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.width, this.height);

    // Subtle dark gradient background
    const bg = ctx.createRadialGradient(this.width / 2, this.height / 2, 10, this.width / 2, this.height / 2, this.width / 2);
    bg.addColorStop(0, '#090d1e');
    bg.addColorStop(1, '#050710');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, this.width, this.height);

    // Render Edges
    this.edges.forEach(edge => {
      const isConnectedToActive = this.activeEntityId && (edge.source.id === this.activeEntityId || edge.target.id === this.activeEntityId);
      ctx.beginPath();
      ctx.moveTo(edge.source.x, edge.source.y);
      ctx.lineTo(edge.target.x, edge.target.y);
      ctx.strokeStyle = isConnectedToActive ? 'rgba(0, 240, 255, 0.7)' : 'rgba(255, 255, 255, 0.12)';
      ctx.lineWidth = isConnectedToActive ? 2 : 1;
      ctx.stroke();
    });

    // Render Nodes
    this.nodes.forEach(node => {
      const isActive = node.id === this.activeEntityId;
      const isHovered = this.hoveredNode && this.hoveredNode.id === node.id;

      // Pulse decay
      if (node.pulse > 0) {
        node.pulse -= 0.015;
      }

      // Outer Glow
      if (isActive || node.pulse > 0 || isHovered) {
        ctx.beginPath();
        const glowRadius = node.r + 10 + (node.pulse * 12);
        ctx.arc(node.x, node.y, glowRadius, 0, Math.PI * 2);
        ctx.fillStyle = isActive ? 'rgba(0, 240, 255, 0.25)' : 'rgba(168, 85, 247, 0.2)';
        ctx.fill();
      }

      // Main Node Circle
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
      ctx.fillStyle = isActive ? '#00f0ff' : (node.category === 'technology' ? '#38bdf8' : (node.category === 'concept' ? '#c084fc' : '#34d399'));
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Node Label
      ctx.fillStyle = isActive || isHovered ? '#ffffff' : '#94a3b8';
      ctx.font = '600 10px "Plus Jakarta Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(node.label, node.x, node.y + node.r + 14);
    });
  }
}

window.KnowledgeGraphVisualizer = KnowledgeGraphVisualizer;
