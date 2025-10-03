// static/js/chat.js
(function () {
  const win = document.getElementById('chatWindow');
  const form = document.getElementById('chatForm');
  const input = document.getElementById('chatInput');
  const micBtn = document.getElementById('micBtn');
  const voiceStatus = document.getElementById('voiceStatus');

  if (!win || !form || !input) return;

  function addMessage(text, role = 'bot') {
    const wrap = document.createElement('div');
    wrap.className = `max-w-[85%] rounded-2xl px-3 py-2 ${role === 'user'
      ? 'bg-emerald-600 text-white ml-auto'
      : 'bg-slate-100'
    }`;
    wrap.innerText = text;
    win.appendChild(wrap);
    win.scrollTop = win.scrollHeight;
  }

  function addTyping() {
    const t = document.createElement('div');
    t.className = 'max-w-[60%] bg-slate-100 rounded-2xl px-3 py-2 text-slate-500 text-sm typing';
    t.innerText = 'PazBot está escribiendo…';
    win.appendChild(t);
    win.scrollTop = win.scrollHeight;
    return t;
  }

  function generateReply(msg) {
    const m = msg.toLowerCase();

    if (m.includes('reconcili')) {
      return 'La reconciliación en Antioquia se fortalece con diálogo, memoria y proyectos comunitarios. ¿Quieres ideas para aplicarla en tu colegio/barrio?';
    }
    if (m.includes('víctima') || m.includes('victima')) {
      return 'El enfoque con víctimas prioriza verdad, reparación y no repetición. Puedo sugerirte actividades pedagógicas de memoria y empatía.';
    }
    if (m.includes('juventud') || m.includes('joven')) {
      return 'La participación juvenil es clave: veedurías escolares, mediación de conflictos y proyectos culturales. Te puedo dar un plan en 5 pasos.';
    }
    if (m.includes('territorio') || m.includes('comuna') || m.includes('vereda')) {
      return 'Los “territorios de paz” se construyen con acuerdos básicos de convivencia, mapeo de conflictos y acciones colectivas. ¿Te propongo un canvas rápido?';
    }
    if (m.includes('comunicación') || m.includes('no violenta') || m.includes('cnv')) {
      return 'Tip CNV: observa sin juzgar, expresa sentimientos, identifica necesidades y haz peticiones claras. ¿Practicamos con un ejemplo?';
    }
    if (m.includes('antioquia')) {
      return 'En Antioquia hay experiencias valiosas de paz comunitaria y escolar. ¿Te resumo 3 prácticas replicables para tu contexto?';
    }
    return 'Gracias por tu mensaje 💚. Mientras conectamos el modelo, te puedo guiar con buenas prácticas de diálogo, mediación y participación ciudadana. ¿Qué situación concreta quieres abordar?';
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = (input.value || '').trim();
    if (!text) return;

    addMessage(text, 'user');
    input.value = '';

    const typing = addTyping();
    setTimeout(() => {
      typing.remove();
      const reply = generateReply(text);
      addMessage(reply, 'bot');
    }, 900 + Math.random() * 600);
  });

  document.querySelectorAll('.tema-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      input.value = `Quiero hablar sobre ${btn.textContent.trim()} en Antioquia.`;
      input.focus();
    });
  });

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recognition = null;
  let listening = false;

  function setListening(on) {
    listening = on;
    if (voiceStatus) voiceStatus.classList.toggle('hidden', !on);
    if (micBtn) micBtn.classList.toggle('bg-emerald-100', on);
  }

  if (SpeechRecognition && micBtn) {
    recognition = new SpeechRecognition();
    recognition.lang = 'es-CO';
    recognition.interimResults = true;
    recognition.continuous = false;

    recognition.onstart = () => setListening(true);
    recognition.onend = () => {
      setListening(false);
      const txt = (input.value || '').trim();
      if (txt) form.dispatchEvent(new Event('submit', { cancelable: true }));
    };
    recognition.onresult = (event) => {
      let transcript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      input.value = transcript.trim();
    };

    micBtn.addEventListener('click', () => {
      if (!listening) recognition.start();
      else recognition.stop();
    });
  } else if (micBtn) {
    micBtn.addEventListener('click', () => {
      alert('Tu navegador no soporta reconocimiento de voz (Web Speech API). Prueba con Chrome/Edge en escritorio.');
    });
  }
})();
