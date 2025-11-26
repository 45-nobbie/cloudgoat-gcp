const API_BASE = 'http://localhost:4000/api';
async function fetchJSON(url, opts) {
  const r = await fetch(url, opts);
  const t = await r.text();
  try { return JSON.parse(t); } catch(e) { return t; }
}

async function loadChallenges() {
  const listEl = document.getElementById('challenge-list');
  listEl.innerHTML = 'Loading…';
  try {
    const data = await fetchJSON(API_BASE + '/challenges');
    if (!Array.isArray(data)) throw new Error('Bad response');
    listEl.innerHTML = '';
    const sel = document.getElementById('challenge');
    sel.innerHTML = '';
    data.forEach(ch => {
      const node = document.createElement('div');
      node.className = 'card';
      node.innerHTML = `
        <h3>${ch.title} <span class="small">[${ch.points} pts]</span></h3>
        <p>${ch.summary || ''}</p>
        <button type="button" onclick="deployChallenge('${ch.id}')">Deploy</button>
        <div class="hints"><strong>Hints:</strong>
          ${ (ch.hints || []).slice(0,2).map(h=>`<div class="hint">${h}</div>`).join('') }
        </div>`;
      listEl.appendChild(node);

      const opt = document.createElement('option');
      opt.value = ch.id;
      opt.textContent = ch.title;
      sel.appendChild(opt);
    });
  } catch (err) {
    listEl.innerHTML = `<div class="card">Failed to load challenges: ${err.message}</div>`;
  }
}

async function submitFlag() {
  const ch = document.getElementById('challenge').value;
  const flag = document.getElementById('flag').value.trim();
  const result = document.getElementById('result');
  result.className = '';
  result.textContent = 'Submitting…';
  try {
    const res = await fetchJSON(API_BASE + '/submit-flag', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({challengeId: ch, flag})
    });
    if (res && res.success) {
      result.className = 'success';
      result.textContent = `Accepted — ${res.message || 'Well done.'}`;
    } else {
      result.className = 'error';
      result.textContent = `Rejected — ${res.message || JSON.stringify(res)}`;
    }
  } catch (e) {
    result.className = 'error';
    result.textContent = 'Error submitting flag: ' + e.message;
  }
}

async function deployChallenge(id, ev) {
  if (ev && ev.preventDefault) ev.preventDefault();
  try {
    const res = await fetch(`${API_BASE}/challenges/${id}/deploy`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ action: "start" })
    });
    if (!res.ok) {
      const text = await res.text();
      alert("Deploy failed: " + text);
      return;
    }
    const data = await res.json();
    alert(data.message);
  } catch (e) {
    alert("Failed to deploy challenge: " + e.message);
  }
}




document.getElementById('submit-btn').addEventListener('click', submitFlag);
loadChallenges();
