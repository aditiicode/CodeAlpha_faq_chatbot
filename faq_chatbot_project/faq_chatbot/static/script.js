const form = document.getElementById('chat-form');
const textarea = document.getElementById('question');
const messages = document.getElementById('messages');
const sendButton = document.getElementById('send');

function addMessage(text, role, matched = '') {
  const row = document.createElement('div');
  row.className = `message ${role}`;
  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = role === 'bot' ? 'Q' : 'You';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  const p = document.createElement('p');
  p.textContent = text;
  bubble.appendChild(p);
  if (matched) {
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = `Matched FAQ: ${matched}`;
    bubble.appendChild(meta);
  }
  row.append(avatar, bubble);
  messages.appendChild(row);
  messages.scrollTop = messages.scrollHeight;
}

async function sendQuestion(question) {
  const q = question.trim();
  if (!q) return;
  addMessage(q, 'user');
  textarea.value = '';
  textarea.style.height = 'auto';
  sendButton.disabled = true;
  const typing = document.createElement('div');
  typing.className = 'message bot typing';
  typing.innerHTML = '<div class="avatar">Q</div><div class="bubble">Finding the closest FAQ...</div>';
  messages.appendChild(typing);
  messages.scrollTop = messages.scrollHeight;
  try {
    const response = await fetch('/chat', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q })
    });
    const data = await response.json();
    typing.remove();
    addMessage(data.answer, 'bot', data.matched_question || 'No close match');
  } catch (error) {
    typing.remove();
    addMessage('Unable to connect to the chatbot. Please try again.', 'bot');
  } finally {
    sendButton.disabled = false;
    textarea.focus();
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  sendQuestion(textarea.value);
});
textarea.addEventListener('input', () => {
  textarea.style.height = 'auto';
  textarea.style.height = `${Math.min(textarea.scrollHeight, 130)}px`;
});
textarea.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});
document.querySelectorAll('.suggestion').forEach(button => {
  button.addEventListener('click', () => sendQuestion(button.dataset.question));
});
