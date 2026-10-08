/* ============================================================
   kisan-app.js — Kisan AI SPA Router & Voice Assistant
   ============================================================

   Handles:
   - SPA navigation / page routing
   - Mobile hamburger menu
   - Voice assistant overlay (integrates with existing app.js API)
   - Form submissions
   - Micro-interactions & animations
   ============================================================ */

"use strict";

/* ─── Router ────────────────────────────────────────────────── */
const Router = (() => {
  const PAGES = ['overview', 'crop-intelligence', 'disease-detection', 'weather-platform', 'technology', 'contact'];
  let _current = 'overview';

  function navigate(pageId) {
    if (!PAGES.includes(pageId)) pageId = 'overview';
    if (pageId === _current) return;

    // Hide current
    const prevEl = document.getElementById(`page-${_current}`);
    if (prevEl) prevEl.classList.add('hidden');

    // Show new
    const nextEl = document.getElementById(`page-${pageId}`);
    if (nextEl) {
      nextEl.classList.remove('hidden');
      // Trigger re-animation
      nextEl.style.animation = 'none';
      nextEl.offsetHeight; // reflow
      nextEl.style.animation = '';
    }

    // Update nav links
    document.querySelectorAll('.nav-link, .mobile-nav-link, .footer-link').forEach(link => {
      const linkPage = link.dataset.page;
      if (linkPage) {
        link.classList.toggle('nav-link--active', linkPage === pageId);
      }
    });

    // Update URL hash
    history.pushState({ page: pageId }, '', `#${pageId}`);
    _current = pageId;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Close mobile nav
    MobileNav.close();
  }

  function init() {
    // Handle initial hash
    const hash = window.location.hash.slice(1);
    if (hash && PAGES.includes(hash)) {
      _current = hash;
      document.getElementById(`page-overview`)?.classList.add('hidden');
      document.getElementById(`page-${hash}`)?.classList.remove('hidden');
      document.querySelectorAll('.nav-link').forEach(l => {
        l.classList.toggle('nav-link--active', l.dataset.page === hash);
      });
    }

    // Delegate click on any element with data-page attribute
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-page]');
      if (trigger) {
        e.preventDefault();
        navigate(trigger.dataset.page);
      }
    });

    // Browser back/forward
    window.addEventListener('popstate', (e) => {
      if (e.state && e.state.page) {
        const curr = _current;
        _current = e.state.page; // temp
        _current = curr; // reset so navigate() runs
        navigate(e.state.page);
      }
    });
  }

  return { init, navigate, current: () => _current };
})();


/* ─── Mobile Nav ─────────────────────────────────────────────── */
const MobileNav = (() => {
  let btn, nav;

  function open() {
    nav.classList.add('open');
    btn.setAttribute('aria-expanded', 'true');
  }

  function close() {
    nav.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
  }

  function toggle() {
    nav.classList.contains('open') ? close() : open();
  }

  function init() {
    btn = document.getElementById('hamburger-btn');
    nav = document.getElementById('mobile-nav');
    if (!btn || !nav) return;
    btn.addEventListener('click', toggle);
    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!btn.contains(e.target) && !nav.contains(e.target)) close();
    });
  }

  return { init, open, close };
})();


/* ─── Header Scroll Effect ───────────────────────────────────── */
const HeaderScroll = (() => {
  let header;
  let lastY = 0;

  function init() {
    header = document.getElementById('site-header');
    if (!header) return;
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  function onScroll() {
    const y = window.scrollY;
    if (y > 50) {
      header.style.boxShadow = '0 2px 16px rgba(0,0,0,0.08)';
    } else {
      header.style.boxShadow = '';
    }
    lastY = y;
  }

  return { init };
})();


/* ─── Voice Assistant Overlay ────────────────────────────────── */
const VoiceAssistant = (() => {
  let overlay, closeBtn, micBtn, voiceIcon, statusText, transcript, chat, textInput, sendBtn;
  let isRecording = false;
  let stream = null;

  function open() {
    if (!overlay) return;
    overlay.classList.remove('hidden');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    textInput.focus();
  }

  function close() {
    if (!overlay) return;
    overlay.classList.add('hidden');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (isRecording) stopRecording();
  }

  function startRecording() {
    if (typeof SpeechInput === 'undefined') {
      addBotMessage("Voice recording is not available. Please type your question.");
      return;
    }

    isRecording = true;
    voiceIcon.classList.add('recording');
    micBtn.classList.add('active');
    statusText.textContent = 'Listening... Speak in Marathi, Hindi, or English';
    transcript.textContent = '';

    SpeechInput.startRecording({
      onInterim: (text) => {
        transcript.textContent = text;
      },
      onFinal: async (blob) => {
        statusText.textContent = 'Processing...';
        try {
          const result = await API.speechToText(blob);
          const userText = result.marathi_text || result.text || '';
          const englishText = result.english_text || '';

          if (userText) {
            addUserMessage(userText);
            transcript.textContent = '';
          }

          if (englishText || userText) {
            statusText.textContent = 'Generating response...';
            const chatResp = await API.chat(englishText || userText);
            const replyText = chatResp.marathi_text || chatResp.reply || chatResp.text || '';
            if (replyText) addBotMessage(replyText);
          }
        } catch (err) {
          addBotMessage("माफ करा, एक त्रुटी झाली. कृपया पुन्हा प्रयत्न करा. (Sorry, an error occurred. Please try again.)");
          console.error('Voice processing error:', err);
        } finally {
          statusText.textContent = 'Hold the button and speak in Marathi, Hindi, or English';
        }
      },
      onError: (msg) => {
        addBotMessage(msg);
        stopRecordingUI();
      }
    });
  }

  function stopRecording() {
    if (typeof SpeechInput !== 'undefined' && SpeechInput.isRecording()) {
      SpeechInput.stopRecording();
    }
    stopRecordingUI();
  }

  function stopRecordingUI() {
    isRecording = false;
    voiceIcon.classList.remove('recording');
    micBtn.classList.remove('active');
    statusText.textContent = 'Hold the button and speak in Marathi, Hindi, or English';
  }

  async function sendText() {
    const text = textInput.value.trim();
    if (!text) return;
    textInput.value = '';
    addUserMessage(text);
    statusText.textContent = 'Generating response...';

    try {
      let resp;
      if (typeof API !== 'undefined') {
        resp = await API.chat(text);
        const reply = resp.marathi_text || resp.reply || resp.text || '';
        if (reply) addBotMessage(reply);
        else addBotMessage('मला उत्तर सापडले नाही. (I could not find an answer.)');
      } else {
        // Fallback mock
        addBotMessage('Kisan AI is connecting to the backend. Please ensure the backend server is running.');
      }
    } catch (err) {
      addBotMessage('माफ करा, सर्व्हरशी कनेक्ट होता आले नाही. (Could not connect to server.)');
    } finally {
      statusText.textContent = 'Hold the button and speak in Marathi, Hindi, or English';
    }
  }

  function addUserMessage(text) {
    const msg = document.createElement('div');
    msg.className = 'voice-chat-msg voice-chat-msg--user';
    msg.textContent = text;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
  }

  function addBotMessage(text) {
    const msg = document.createElement('div');
    msg.className = 'voice-chat-msg voice-chat-msg--bot';
    msg.textContent = text;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
  }

  function init() {
    overlay    = document.getElementById('voice-overlay');
    closeBtn   = document.getElementById('voice-close-btn');
    micBtn     = document.getElementById('voice-mic-btn');
    voiceIcon  = document.getElementById('voice-icon');
    statusText = document.getElementById('voice-status-text');
    transcript = document.getElementById('voice-transcript');
    chat       = document.getElementById('voice-chat');
    textInput  = document.getElementById('voice-text-input');
    sendBtn    = document.getElementById('voice-send-btn');

    if (!overlay) return;

    // Open triggers
    document.getElementById('voice-assistant-btn')?.addEventListener('click', open);
    document.getElementById('voice-demo-btn')?.addEventListener('click', open);
    document.getElementById('voice-query-btn')?.addEventListener('click', open);

    // Close
    closeBtn?.addEventListener('click', close);
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) close();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close();
    });

    // Mic button: hold to record
    micBtn?.addEventListener('mousedown', startRecording);
    micBtn?.addEventListener('mouseup', stopRecording);
    micBtn?.addEventListener('touchstart', (e) => { e.preventDefault(); startRecording(); }, { passive: false });
    micBtn?.addEventListener('touchend', (e) => { e.preventDefault(); stopRecording(); }, { passive: false });

    // Text send
    sendBtn?.addEventListener('click', sendText);
    textInput?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendText();
      }
    });

    // Initial bot greeting
    setTimeout(() => {
      addBotMessage('नमस्कार! मी Kisan AI आहे. आपल्या शेतीसंबंधी प्रश्न विचारा. (Hello! I am Kisan AI. Ask me about your farming needs.)');
    }, 300);
  }

  return { init, open, close };
})();


/* ─── Form Handlers ──────────────────────────────────────────── */
const Forms = (() => {
  function handleSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;

    btn.disabled = true;
    btn.innerHTML = '<span class="material-symbols-outlined" style="animation:spin 1s linear infinite">refresh</span> Submitting...';

    setTimeout(() => {
      btn.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Request Received!';
      btn.style.background = 'var(--c-secondary)';
      form.reset();
      setTimeout(() => {
        btn.disabled = false;
        btn.innerHTML = originalText;
        btn.style.background = '';
      }, 3000);
    }, 1200);
  }

  function init() {
    document.getElementById('pilot-form')?.addEventListener('submit', handleSubmit);
    document.getElementById('contact-form')?.addEventListener('submit', handleSubmit);
  }

  return { init };
})();


/* ─── Animations & Micro-interactions ───────────────────────── */
const Animations = (() => {
  function observeIntersection() {
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    document.querySelectorAll('.feature-card, .crop-card, .pipeline-step, .metric-card, .tech-module').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(16px)';
      el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      observer.observe(el);
    });
  }

  function addCSSForVisible() {
    const style = document.createElement('style');
    style.textContent = `.visible { opacity: 1 !important; transform: translateY(0) !important; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`;
    document.head.appendChild(style);
  }

  function init() {
    addCSSForVisible();
    // Run after a brief delay to ensure DOM is rendered
    setTimeout(observeIntersection, 100);

    // Re-run on navigation (page changes)
    window.addEventListener('popstate', () => setTimeout(observeIntersection, 150));
  }

  return { init };
})();


/* ─── Health Status Check ────────────────────────────────────── */
const HealthCheck = (() => {
  async function check() {
    if (typeof API === 'undefined') return;
    try {
      const result = await API.healthCheck();
      if (result && result.status) {
        console.log('Backend status:', result.status);
      }
    } catch (e) {
      console.warn('Backend not reachable. Voice features require backend to be running.');
    }
  }

  function init() {
    check();
  }

  return { init };
})();


/* ─── Service Worker Registration ────────────────────────────── */
const PWA = (() => {
  function init() {
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(err => {
          // SW not critical — ignore errors
        });
      });
    }
  }
  return { init };
})();


/* ─── Main Boot ──────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  Router.init();
  MobileNav.init();
  HeaderScroll.init();
  VoiceAssistant.init();
  Forms.init();
  Animations.init();
  HealthCheck.init();
  PWA.init();

  console.log('🌾 Kisan AI Platform ready. Hyperlocal telemetry active.');
});
