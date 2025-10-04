// static/js/chat.js
(function () {
  const win = document.getElementById('chatWindow');
  const form = document.getElementById('chatForm');
  const input = document.getElementById('chatInput');
  const micBtn = document.getElementById('micBtn');
  const voiceStatus = document.getElementById('voiceStatus');
  const newChatBtn = document.getElementById('newChatBtn');
  const sessionIdInput = document.getElementById('sessionId');

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

  async function sendMessage(message) {
    const sessionId = sessionIdInput.value;
    
    try {
      const response = await fetch('/chat/message/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          session_id: sessionId
        })
      });

      const data = await response.json();
      
      if (data.success) {
        return data.response;
      } else {
        throw new Error(data.error || 'Error desconocido');
      }
    } catch (error) {
      console.error('Error:', error);
      return 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente. 🌿';
    }
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = (input.value || '').trim();
    if (!text) return;

    addMessage(text, 'user');
    input.value = '';

    const typing = addTyping();
    const reply = await sendMessage(text);
    typing.remove();
    addMessage(reply, 'bot');
  });

  document.querySelectorAll('.tema-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      input.value = `Quiero hablar sobre ${btn.textContent.trim()} en Antioquia.`;
      input.focus();
    });
  });

  // Nueva conversación
  if (newChatBtn) {
    newChatBtn.addEventListener('click', async () => {
      try {
        const response = await fetch('/chat/new/', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
          window.location.reload();
        }
      } catch (error) {
        console.error('Error al crear nueva conversación:', error);
      }
    });
  }

  // Reconocimiento de voz
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
