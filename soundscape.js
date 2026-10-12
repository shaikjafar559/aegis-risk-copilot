/**
 * OmniStory Web Audio Procedural Soundscape Engine
 * Generates dynamic studio room ambiance, binaural chords, and transition audio cues.
 */
class StudioSoundscape {
  constructor() {
    this.ctx = null;
    this.isPlaying = false;
    this.masterGain = null;
    this.oscillators = [];
    this.filter = null;
    this.lfo = null;
    this.isMuted = false;
  }

  init() {
    if (this.ctx) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioCtx();

      // Master Gain
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.setValueAtTime(0.045, this.ctx.currentTime); // gentle background ambient level
      this.masterGain.connect(this.ctx.destination);

      // Lowpass Filter for warm broadcast tone
      this.filter = this.ctx.createBiquadFilter();
      this.filter.type = 'lowpass';
      this.filter.frequency.setValueAtTime(420, this.ctx.currentTime);
      this.filter.connect(this.masterGain);

      // Harmonic chords (D-minor / futuristic ambient stack: D2, A2, F3)
      const baseFreqs = [73.42, 110.0, 174.61]; // D2, A2, F3

      baseFreqs.forEach(freq => {
        const osc = this.ctx.createOscillator();
        const oscGain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        oscGain.gain.setValueAtTime(0.3, this.ctx.currentTime);

        osc.connect(oscGain);
        oscGain.connect(this.filter);
        osc.start();
        this.oscillators.push(osc);
      });

      // LFO filter sweep for breathing atmosphere
      this.lfo = this.ctx.createOscillator();
      const lfoGain = this.ctx.createGain();
      this.lfo.frequency.setValueAtTime(0.12, this.ctx.currentTime); // Very slow 8-second swell
      lfoGain.gain.setValueAtTime(140, this.ctx.currentTime);

      this.lfo.connect(lfoGain);
      lfoGain.connect(this.filter.frequency);
      this.lfo.start();

      this.isPlaying = true;
    } catch (e) {
      console.warn('Web Audio not yet initialized or supported:', e);
    }
  }

  toggle(enabled) {
    if (!this.ctx && enabled) {
      this.init();
      return true;
    }
    if (!this.ctx) return false;

    if (enabled) {
      if (this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      this.masterGain.gain.setTargetAtTime(0.045, this.ctx.currentTime, 0.5);
      this.isPlaying = true;
    } else {
      this.masterGain.gain.setTargetAtTime(0.0001, this.ctx.currentTime, 0.5);
      this.isPlaying = false;
    }
    return this.isPlaying;
  }

  playCue(type = 'ping') {
    if (!this.ctx || !this.isPlaying) return;
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      if (type === 'speaker_switch') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(587.33, this.ctx.currentTime); // D5
        osc.frequency.exponentialRampToValueAtTime(880.0, this.ctx.currentTime + 0.12);
        gain.gain.setValueAtTime(0.03, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.18);
      } else if (type === 'interrupt') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(329.63, this.ctx.currentTime); // E4
        osc.frequency.exponentialRampToValueAtTime(659.25, this.ctx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.06, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.25);
      } else {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, this.ctx.currentTime);
        gain.gain.setValueAtTime(0.02, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.15);
      }

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.3);
    } catch (e) {
      // Quiet fail if audio blocked
    }
  }
}

window.StudioSoundscape = StudioSoundscape;
