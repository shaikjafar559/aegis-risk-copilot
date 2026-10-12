/**
 * OmniStory Studio Main Application Controller
 * Orchestrates multi-agent voice playback, interactive interruptions, narrative branching, and omnichannel exports.
 */
document.addEventListener('DOMContentLoaded', () => {
  // State
  let currentManifest = null;
  let currentLineIndex = 0;
  let isPlaying = false;
  let voicesEnabled = true;
  let bgmEnabled = true;
  let speechSynth = window.speechSynthesis;
  let activeUtterance = null;
  let fallbackTimer = null;

  // Subsystems
  const visualizer = new StudioVisualizer('generativeCanvas');
  const soundscape = new StudioSoundscape();
  const kgVisualizer = new KnowledgeGraphVisualizer('kgCanvas');

  // DOM Elements
  const broadcastSelect = document.getElementById('broadcastSelect');
  const btnDirectorMode = document.getElementById('btnDirectorMode');
  const directorDrawer = document.getElementById('directorDrawer');
  const btnCloseDrawer = document.getElementById('btnCloseDrawer');
  const btnSynthesizeCustom = document.getElementById('btnSynthesizeCustom');
  const genSpinner = document.getElementById('genSpinner');

  const inputTopic = document.getElementById('inputTopic');
  const inputRawNotes = document.getElementById('inputRawNotes');
  const selectPersona = document.getElementById('selectPersona');

  const hostMaya = document.getElementById('hostMaya');
  const hostLeo = document.getElementById('hostLeo');
  const mayaStatus = document.getElementById('mayaStatus');
  const leoStatus = document.getElementById('leoStatus');

  const activeSpeakerBadge = document.getElementById('activeSpeakerBadge');
  const teleprompterText = document.getElementById('teleprompterText');
  const teleprompterTags = document.getElementById('teleprompterTags');
  const sceneBadge = document.getElementById('sceneBadge');
  const chapterBadge = document.getElementById('chapterBadge');

  const btnPlayPause = document.getElementById('btnPlayPause');
  const playIcon = document.getElementById('playIcon');
  const pauseIcon = document.getElementById('pauseIcon');
  const btnPrevLine = document.getElementById('btnPrevLine');
  const btnNextLine = document.getElementById('btnNextLine');
  const btnRestart = document.getElementById('btnRestart');
  const timelineTrack = document.getElementById('timelineTrack');
  const timelineFill = document.getElementById('timelineFill');
  const currentTimeDisplay = document.getElementById('currentTimeDisplay');
  const activeTopicTitle = document.getElementById('activeTopicTitle');
  const estimatedDuration = document.getElementById('estimatedDuration');

  const btnVoiceToggle = document.getElementById('btnVoiceToggle');
  const btnBgmToggle = document.getElementById('btnBgmToggle');
  const soundscapeBadge = document.getElementById('soundscapeBadge');

  const inputInterrupt = document.getElementById('inputInterrupt');
  const btnSendInterrupt = document.getElementById('btnSendInterrupt');
  const quickButtons = document.querySelectorAll('.quick-btn');
  const branchCardsGrid = document.getElementById('branchCardsGrid');

  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');
  const perspectiveList = document.getElementById('perspectiveList');
  const transcriptList = document.getElementById('transcriptList');
  const scriptLineCount = document.getElementById('scriptLineCount');

  const entityDetailTitle = document.getElementById('entityDetailTitle');
  const entityDetailCategory = document.getElementById('entityDetailCategory');
  const entityDetailDesc = document.getElementById('entityDetailDesc');

  // Export Modal Elements
  const btnExportModal = document.getElementById('btnExportModal');
  const exportModal = document.getElementById('exportModal');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const expTabBtns = document.querySelectorAll('.exp-tab-btn');
  const expPanes = document.querySelectorAll('.exp-pane');
  const briefExportArea = document.getElementById('briefExportArea');
  const jsonExportArea = document.getElementById('jsonExportArea');
  const socialTwitter = document.getElementById('socialTwitter');
  const socialLinkedin = document.getElementById('socialLinkedin');
  const socialShort = document.getElementById('socialShort');
  const btnCopyBrief = document.getElementById('btnCopyBrief');
  const btnCopyJson = document.getElementById('btnCopyJson');
  const studioToast = document.getElementById('studioToast');

  // Voice setup
  let voices = [];
  function populateVoices() {
    if (!speechSynth) return;
    voices = speechSynth.getVoices();
  }
  populateVoices();
  if (speechSynth && speechSynth.onvoiceschanged !== undefined) {
    speechSynth.onvoiceschanged = populateVoices;
  }

  function getSpeakerVoice(speaker) {
    if (!voices || voices.length === 0) return null;
    const lang = 'en';

    if (speaker === 'maya') {
      // Prefer female English voice
      const mayaVoice = voices.find(v => v.lang.startsWith(lang) && (v.name.includes('Zira') || v.name.includes('Samantha') || v.name.includes('Female') || v.name.includes('Jenny') || v.name.includes('Google US English')));
      return mayaVoice || voices.find(v => v.lang.startsWith(lang)) || voices[0];
    } else if (speaker === 'leo') {
      // Prefer male English voice
      const leoVoice = voices.find(v => v.lang.startsWith(lang) && (v.name.includes('David') || v.name.includes('Guy') || v.name.includes('Male') || v.name.includes('George') || v.name.includes('Google UK English Male')));
      return leoVoice || voices.find(v => v.lang.startsWith(lang)) || voices[0];
    } else {
      // Narrator / System
      const narrVoice = voices.find(v => v.lang.startsWith(lang) && (v.name.includes('Mark') || v.name.includes('Natural') || v.name.includes('English')));
      return narrVoice || voices[0];
    }
  }

  function showToast(msg) {
    studioToast.textContent = msg;
    studioToast.classList.remove('hidden');
    setTimeout(() => {
      studioToast.classList.add('hidden');
    }, 2800);
  }

  // Load Broadcast
  async function loadBroadcast(id) {
    stopPlayback();
    try {
      const res = await fetch(`/api/broadcasts/${id}`);
      if (!res.ok) throw new Error('Failed to fetch broadcast');
      currentManifest = await res.json();
      currentLineIndex = 0;
      renderBroadcastManifest();
      showToast(`Loaded: ${currentManifest.title}`);
    } catch (err) {
      console.error(err);
      showToast('Error loading broadcast manifest.');
    }
  }

  function renderBroadcastManifest() {
    if (!currentManifest) return;

    activeTopicTitle.textContent = currentManifest.title.split(':')[0];
    estimatedDuration.textContent = `Est: ${currentManifest.duration_est}`;

    // Render Branches
    branchCardsGrid.innerHTML = '';
    currentManifest.branches.forEach(branch => {
      const card = document.createElement('div');
      card.className = 'branch-card';
      card.innerHTML = `
        <div class="branch-card-title">
          <span>${branch.title}</span>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        </div>
        <div class="branch-card-desc">${branch.description}</div>
      `;
      card.addEventListener('click', () => activateBranch(branch.id));
      branchCardsGrid.appendChild(card);
    });

    // Render Knowledge Graph
    kgVisualizer.setData(currentManifest.knowledge_graph, (entity) => {
      entityDetailTitle.textContent = entity.label;
      entityDetailCategory.textContent = entity.category.toUpperCase();
      entityDetailDesc.textContent = entity.description;
    });

    // Render Perspectives
    perspectiveList.innerHTML = '';
    currentManifest.perspectives.forEach(p => {
      const item = document.createElement('div');
      item.className = 'perspective-item';
      item.innerHTML = `
        <div class="perspective-meta">
          <span class="persp-dim">${p.dimension}</span>
          <span class="persp-score">${p.score}/100</span>
        </div>
        <div class="persp-bar-track">
          <div class="persp-bar-fill" style="width: ${p.score}%"></div>
        </div>
        <div class="persp-summary">${p.summary}</div>
      `;
      perspectiveList.appendChild(item);
    });

    // Render Transcript Lines
    renderTranscriptList();

    // Display first line in teleprompter
    displayCurrentLine(false);
  }

  function renderTranscriptList() {
    transcriptList.innerHTML = '';
    scriptLineCount.textContent = `${currentManifest.lines.length} Lines`;
    currentManifest.lines.forEach((line, idx) => {
      const el = document.createElement('div');
      el.className = `transcript-line ${idx === currentLineIndex ? 'active' : ''}`;
      el.dataset.index = idx;
      el.innerHTML = `
        <div class="tl-header">
          <span class="tl-speaker">${line.speaker_name}</span>
          <span class="tl-time">~0:${String(line.timestamp_est).padStart(2, '0')}</span>
        </div>
        <div class="tl-text">${line.text}</div>
      `;
      el.addEventListener('click', () => {
        jumpToLine(idx);
      });
      transcriptList.appendChild(el);
    });
  }

  function displayCurrentLine(triggerSpeech = true) {
    if (!currentManifest || !currentManifest.lines[currentLineIndex]) return;

    const line = currentManifest.lines[currentLineIndex];

    // Update Teleprompter
    activeSpeakerBadge.textContent = line.speaker_name.toUpperCase();
    activeSpeakerBadge.style.color = line.speaker === 'maya' ? 'var(--cyan-primary)' : (line.speaker === 'leo' ? 'var(--purple-primary)' : '#cbd5e1');

    // Highlight key terms in teleprompter text
    let formattedText = line.text;
    if (line.highlight_terms && line.highlight_terms.length > 0) {
      line.highlight_terms.forEach(term => {
        const regex = new RegExp(`(${term})`, 'gi');
        formattedText = formattedText.replace(regex, `<span class="term-highlight">$1</span>`);
      });
    }
    teleprompterText.innerHTML = formattedText;

    // Add interactive click to highlighted terms
    teleprompterText.querySelectorAll('.term-highlight').forEach(el => {
      el.addEventListener('click', () => {
        kgVisualizer.highlightByTerm(el.textContent);
      });
    });

    // Update tags
    teleprompterTags.innerHTML = `
      <span class="tag">EMOTION: ${line.emotion.toUpperCase()}</span>
      <span class="tag">CUE: ${line.visual_cue.replace('_', ' ').toUpperCase()}</span>
    `;

    chapterBadge.textContent = `CHAPTER: ${line.chapter.toUpperCase()}`;
    sceneBadge.textContent = `SCENE: ${line.visual_cue.replace('_', ' ').toUpperCase()}`;

    // Update Host Speaking Badges
    hostMaya.classList.remove('speaking');
    hostLeo.classList.remove('speaking');
    mayaStatus.textContent = 'LISTENING';
    leoStatus.textContent = 'LISTENING';

    if (line.speaker === 'maya') {
      hostMaya.classList.add('speaking');
      mayaStatus.textContent = `SPEAKING (${line.emotion.toUpperCase()})`;
    } else if (line.speaker === 'leo') {
      hostLeo.classList.add('speaking');
      leoStatus.textContent = `SPEAKING (${line.emotion.toUpperCase()})`;
    }

    // Update Visualizer
    visualizer.setTheme(line.visual_cue);
    visualizer.setSpeaker(line.speaker, line.emotion);

    // Update Knowledge Graph highlights if terms match
    if (line.highlight_terms && line.highlight_terms.length > 0) {
      kgVisualizer.highlightByTerm(line.highlight_terms[0]);
    }

    // Play subtle sound cue
    if (bgmEnabled) {
      soundscape.playCue('speaker_switch');
    }

    // Update Timeline Progress
    const totalLines = currentManifest.lines.length;
    currentTimeDisplay.textContent = `Line ${currentLineIndex + 1} of ${totalLines}`;
    const progressPercent = ((currentLineIndex + 1) / totalLines) * 100;
    timelineFill.style.width = `${progressPercent}%`;

    // Highlight active in transcript list
    document.querySelectorAll('.transcript-line').forEach((tl, idx) => {
      tl.classList.toggle('active', idx === currentLineIndex);
    });

    if (triggerSpeech && isPlaying) {
      speakCurrentLine();
    }
  }

  function speakCurrentLine() {
    if (!isPlaying) return;
    clearTimeout(fallbackTimer);

    if (speechSynth) {
      speechSynth.cancel();
    }

    const line = currentManifest.lines[currentLineIndex];

    if (!voicesEnabled || !speechSynth) {
      // Simulate line duration based on word count
      const wordCount = line.text.split(/\s+/).length;
      const durationMs = Math.max(2500, wordCount * 320);
      fallbackTimer = setTimeout(() => {
        if (isPlaying) advanceNext();
      }, durationMs);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(line.text);
    const chosenVoice = getSpeakerVoice(line.speaker);
    if (chosenVoice) {
      utterance.voice = chosenVoice;
    }

    utterance.rate = (line.rate || (line.speaker === 'maya' ? 1.03 : 1.06)) * cognitivePacingRate;
    utterance.pitch = line.pitch || (line.speaker === 'maya' ? 1.04 : 0.98);

    utterance.onend = () => {
      if (isPlaying) {
        setTimeout(() => {
          advanceNext();
        }, 500); // 500ms natural conversational pause
      }
    };

    utterance.onerror = (e) => {
      console.warn('SpeechSynthesis error:', e);
      if (isPlaying) {
        setTimeout(() => advanceNext(), 2000);
      }
    };

    activeUtterance = utterance;
    speechSynth.speak(utterance);
  }

  function advanceNext() {
    if (currentLineIndex < currentManifest.lines.length - 1) {
      currentLineIndex++;
      displayCurrentLine(true);
    } else {
      stopPlayback();
      showToast('Broadcast concluded. Select a narrative branch or ask a question!');
    }
  }

  function advancePrev() {
    if (currentLineIndex > 0) {
      currentLineIndex--;
      displayCurrentLine(isPlaying);
    }
  }

  function jumpToLine(index) {
    if (!currentManifest || index < 0 || index >= currentManifest.lines.length) return;
    currentLineIndex = index;
    displayCurrentLine(isPlaying);
  }

  function startPlayback() {
    if (!currentManifest) return;
    isPlaying = true;
    playIcon.classList.add('hidden');
    pauseIcon.classList.remove('hidden');

    if (bgmEnabled) {
      soundscape.toggle(true);
    }

    displayCurrentLine(true);
  }

  function stopPlayback() {
    isPlaying = false;
    clearTimeout(fallbackTimer);
    if (speechSynth) {
      speechSynth.cancel();
    }
    playIcon.classList.remove('hidden');
    pauseIcon.classList.add('hidden');

    hostMaya.classList.remove('speaking');
    hostLeo.classList.remove('speaking');
    mayaStatus.textContent = 'PAUSED';
    leoStatus.textContent = 'PAUSED';
    visualizer.setSpeaker(null, null);
  }

  function togglePlayPause() {
    if (isPlaying) {
      stopPlayback();
    } else {
      startPlayback();
    }
  }

  // Live Interrupt Q&A
  async function triggerInterrupt(questionText) {
    if (!questionText || !questionText.trim()) return;
    const q = questionText.trim();
    inputInterrupt.value = '';

    stopPlayback();
    showToast('Injecting Audience Question to Co-Hosts...');
    soundscape.playCue('interrupt');

    try {
      const currentLine = currentManifest.lines[currentLineIndex] || currentManifest.lines[0];
      const res = await fetch('/api/interrupt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          broadcast_id: currentManifest.id,
          current_line_id: currentLine.id,
          user_question: q
        })
      });

      if (!res.ok) throw new Error('Interrupt failed');
      const data = await res.json();

      // Splice the interruption lines right after the current line
      const injection = data.dialogue_injection;
      currentManifest.lines.splice(currentLineIndex + 1, 0, ...injection);

      renderTranscriptList();
      showToast('Maya & Leo responding to audience live!');

      // Move to the audience question line and resume
      currentLineIndex++;
      startPlayback();
    } catch (err) {
      console.error(err);
      showToast('Failed to deliver live audience interrupt.');
    }
  }

  // Branch Selection
  async function activateBranch(branchId) {
    stopPlayback();
    showToast('Switching Narrative Angle...');
    soundscape.playCue('ping');

    try {
      const res = await fetch('/api/branch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          broadcast_id: currentManifest.id,
          branch_id: branchId
        })
      });

      if (!res.ok) throw new Error('Branch activation failed');
      const data = await res.json();

      // Append new lines to manifest
      const newLines = data.new_lines;
      const startIndex = currentManifest.lines.length;
      currentManifest.lines.push(...newLines);

      renderTranscriptList();
      showToast('Narrative branch stream unlocked!');

      currentLineIndex = startIndex;
      startPlayback();
    } catch (err) {
      console.error(err);
      showToast('Error activating narrative branch.');
    }
  }

  // Omnichannel Export
  async function openExportModal() {
    if (!currentManifest) return;
    try {
      const res = await fetch(`/api/export/${currentManifest.id}`);
      if (!res.ok) throw new Error('Failed to fetch export');
      const data = await res.json();

      briefExportArea.value = data.markdown_export;
      jsonExportArea.textContent = JSON.stringify(data.manifest, null, 2);

      const soc = data.social_assets || {};
      socialTwitter.textContent = soc.thread_post || 'N/A';
      socialLinkedin.textContent = soc.linkedin_take || 'N/A';
      socialShort.textContent = soc.short_script_hook || 'N/A';

      exportModal.classList.remove('hidden');
    } catch (err) {
      console.error(err);
      showToast('Error preparing export package.');
    }
  }

  // Event Listeners
  btnPlayPause.addEventListener('click', togglePlayPause);
  btnNextLine.addEventListener('click', advanceNext);
  btnPrevLine.addEventListener('click', advancePrev);
  btnRestart.addEventListener('click', () => {
    currentLineIndex = 0;
    startPlayback();
  });

  timelineTrack.addEventListener('click', (e) => {
    if (!currentManifest) return;
    const rect = timelineTrack.getBoundingClientRect();
    const ratio = (e.clientX - rect.left) / rect.width;
    const targetIdx = Math.floor(ratio * currentManifest.lines.length);
    jumpToLine(Math.max(0, Math.min(targetIdx, currentManifest.lines.length - 1)));
  });

  btnVoiceToggle.addEventListener('click', () => {
    voicesEnabled = !voicesEnabled;
    btnVoiceToggle.classList.toggle('active', voicesEnabled);
    btnVoiceToggle.querySelector('span').textContent = voicesEnabled ? 'VOICES: ON' : 'VOICES: OFF';
    showToast(voicesEnabled ? 'Neural speech synthesizer enabled' : 'Speech synthesis muted');
  });

  btnBgmToggle.addEventListener('click', () => {
    bgmEnabled = !bgmEnabled;
    btnBgmToggle.classList.toggle('active', bgmEnabled);
    btnBgmToggle.querySelector('span').textContent = bgmEnabled ? 'AMBIENCE: ON' : 'AMBIENCE: OFF';
    soundscape.toggle(bgmEnabled);
    soundscapeBadge.style.opacity = bgmEnabled ? '1' : '0.4';
  });

  broadcastSelect.addEventListener('change', (e) => {
    loadBroadcast(e.target.value);
  });

  btnDirectorMode.addEventListener('click', () => {
    directorDrawer.classList.toggle('hidden');
  });

  btnCloseDrawer.addEventListener('click', () => {
    directorDrawer.classList.add('hidden');
  });

  btnSendInterrupt.addEventListener('click', () => {
    triggerInterrupt(inputInterrupt.value);
  });

  inputInterrupt.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      triggerInterrupt(inputInterrupt.value);
    }
  });

  quickButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      triggerInterrupt(btn.dataset.q);
    });
  });

  // Custom synthesis
  btnSynthesizeCustom.addEventListener('click', async () => {
    const topic = inputTopic.value.trim();
    if (!topic) {
      alert('Please enter a topic or media premise.');
      return;
    }

    genSpinner.classList.remove('hidden');
    btnSynthesizeCustom.disabled = true;

    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: topic,
          raw_content: inputRawNotes.value.trim(),
          persona: selectPersona.value
        })
      });

      if (!res.ok) throw new Error('Generation failed');
      const newManifest = await res.json();

      // Add to select options
      const opt = document.createElement('option');
      opt.value = newManifest.id;
      opt.textContent = `★ ${newManifest.title}`;
      broadcastSelect.appendChild(opt);
      broadcastSelect.value = newManifest.id;

      directorDrawer.classList.add('hidden');
      loadBroadcast(newManifest.id);
      showToast('Custom broadcast compiled & loaded!');
    } catch (err) {
      console.error(err);
      showToast('Synthesis error. Check backend logs.');
    } finally {
      genSpinner.classList.add('hidden');
      btnSynthesizeCustom.disabled = false;
    }
  });

  // Sidebar Tabs
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(btn.dataset.tab).classList.add('active');
    });
  });

  // Export Modal
  btnExportModal.addEventListener('click', openExportModal);
  btnCloseModal.addEventListener('click', () => exportModal.classList.add('hidden'));

  expTabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      expTabBtns.forEach(b => b.classList.remove('active'));
      expPanes.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(btn.dataset.exp).classList.add('active');
    });
  });

  btnCopyBrief.addEventListener('click', () => {
    navigator.clipboard.writeText(briefExportArea.value);
    showToast('Executive brief copied to clipboard!');
  });

  btnCopyJson.addEventListener('click', () => {
    navigator.clipboard.writeText(jsonExportArea.textContent);
    showToast('JSON manifest copied to clipboard!');
  });

  // Accessibility & Cognitive Pacing
  const btnContrastToggle = document.getElementById('btnContrastToggle');
  const selectPacing = document.getElementById('selectPacing');
  let cognitivePacingRate = 1.0;

  if (btnContrastToggle) {
    btnContrastToggle.addEventListener('click', () => {
      document.body.classList.toggle('theme-high-contrast');
      const isHigh = document.body.classList.contains('theme-high-contrast');
      btnContrastToggle.classList.toggle('active', isHigh);
      showToast(isHigh ? 'High-Contrast WCAG 2.1 AAA Enabled' : 'Standard Editorial Theme');
    });
  }

  if (selectPacing) {
    selectPacing.addEventListener('change', (e) => {
      cognitivePacingRate = parseFloat(e.target.value) || 1.0;
      showToast(`Cognitive Pacing: ${e.target.value}x`);
    });
  }

  // Initial Load - Social Impact Showcase
  loadBroadcast('health-equity');
});
