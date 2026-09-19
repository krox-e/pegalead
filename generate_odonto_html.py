import json

try:
    with open("clinicas_odontologicas_leads.json", "r", encoding="utf-8") as f:
        leads = json.load(f)
except Exception:
    leads = []

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel de Prospecção • Clínicas Odontológicas</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b1120;
      --card-bg: rgba(15, 23, 42, 0.85);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #0ea5e9;
      --primary-hover: #0284c7;
      --primary-glow: rgba(14, 165, 233, 0.3);
      --whatsapp-green: #25d366;
      --whatsapp-hover: #1ebd5b;
      --whatsapp-glow: rgba(37, 211, 102, 0.25);
      --accent: #38bdf8;
      --text: #f3f4f6;
      --muted: #94a3b8;
      --success: #10b981;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Inter', sans-serif;
      background-color: var(--bg);
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(14, 165, 233, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(56, 189, 248, 0.06) 0%, transparent 40%);
      color: var(--text);
      min-height: 100vh;
      padding: 2.5rem 1.5rem;
    }

    .container {
      max-width: 1100px;
      margin: 0 auto;
    }

    header {
      text-align: center;
      margin-bottom: 2.5rem;
    }

    .badge-user {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(14, 165, 233, 0.12);
      border: 1px solid rgba(14, 165, 233, 0.3);
      color: #38bdf8;
      padding: 0.4rem 1rem;
      border-radius: 9999px;
      font-size: 0.9rem;
      font-weight: 700;
      margin-bottom: 1rem;
      box-shadow: 0 0 15px rgba(14, 165, 233, 0.15);
    }

    h1 {
      font-family: 'Outfit', sans-serif;
      font-size: 2.5rem;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 0%, #bae6fd 50%, #7dd3fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }

    p.subtitle {
      color: var(--muted);
      font-size: 1.1rem;
      max-width: 700px;
      margin: 0 auto;
      line-height: 1.5;
    }

    /* Stats Grid */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }

    .stat-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 1.1rem;
      padding: 1.35rem;
      backdrop-filter: blur(12px);
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }

    .stat-label {
      font-size: 0.825rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 700;
    }

    .stat-value {
      font-family: 'Outfit', sans-serif;
      font-size: 2rem;
      font-weight: 800;
      color: #fff;
    }

    .stat-value.blue { color: #38bdf8; }
    .stat-value.green { color: var(--whatsapp-green); }
    .stat-value.cyan { color: #22d3ee; }

    /* Safety Box */
    .safety-box {
      background: rgba(14, 165, 233, 0.08);
      border: 1px solid rgba(14, 165, 233, 0.3);
      border-radius: 1.1rem;
      padding: 1.25rem 1.5rem;
      margin-bottom: 2rem;
      display: flex;
      align-items: center;
      gap: 1.25rem;
    }

    .safety-box span.icon {
      font-size: 2rem;
    }

    .safety-box h4 {
      font-family: 'Outfit', sans-serif;
      font-size: 1.1rem;
      color: #38bdf8;
      margin-bottom: 0.25rem;
    }

    .safety-box p {
      font-size: 0.925rem;
      color: #e5e7eb;
      line-height: 1.45;
    }

    /* Controls Bar */
    .controls-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    .tabs {
      display: flex;
      background: rgba(15, 23, 42, 0.9);
      padding: 0.4rem;
      border-radius: 0.85rem;
      border: 1px solid var(--card-border);
      gap: 0.4rem;
    }

    .tab-btn {
      background: transparent;
      border: none;
      color: var(--muted);
      padding: 0.6rem 1.2rem;
      border-radius: 0.6rem;
      font-size: 0.925rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .tab-btn.active {
      background: var(--primary);
      color: #ffffff;
      box-shadow: 0 0 12px var(--primary-glow);
    }

    .search-input {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--card-border);
      border-radius: 0.85rem;
      padding: 0.6rem 1rem;
      color: #fff;
      font-size: 0.95rem;
      outline: none;
      min-width: 240px;
    }

    .search-input:focus {
      border-color: var(--primary);
    }

    /* Leads List */
    .leads-list {
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    .lead-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 1.2rem;
      padding: 1.5rem;
      backdrop-filter: blur(12px);
      transition: all 0.2s ease;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 1.5rem;
      align-items: center;
    }

    .lead-card:hover {
      border-color: rgba(14, 165, 233, 0.4);
      transform: translateY(-2px);
    }

    .lead-card.sent {
      border-color: rgba(16, 185, 129, 0.35);
      background: rgba(16, 185, 129, 0.06);
    }

    .lead-info {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .lead-header {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      flex-wrap: wrap;
    }

    .lead-number {
      font-size: 0.85rem;
      font-weight: 800;
      background: rgba(255, 255, 255, 0.08);
      padding: 0.25rem 0.65rem;
      border-radius: 0.5rem;
      color: var(--muted);
    }

    .lead-name {
      font-family: 'Outfit', sans-serif;
      font-size: 1.3rem;
      font-weight: 700;
      color: #ffffff;
    }

    .rating-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      background: rgba(255, 184, 77, 0.12);
      color: #ffb84d;
      padding: 0.25rem 0.6rem;
      border-radius: 0.5rem;
      font-size: 0.875rem;
      font-weight: 700;
    }

    .lead-details {
      display: flex;
      flex-wrap: wrap;
      gap: 1.25rem;
      font-size: 0.9rem;
      color: var(--muted);
    }

    .detail-item {
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }

    .detail-item strong {
      color: #e5e7eb;
    }

    .msg-preview {
      background: rgba(11, 17, 32, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 0.75rem;
      padding: 0.85rem 1.1rem;
      font-size: 0.875rem;
      color: #e2e8f0;
      line-height: 1.5;
      margin-top: 0.35rem;
      white-space: pre-line;
      max-height: 130px;
      overflow-y: auto;
    }

    /* Actions */
    .lead-actions {
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      min-width: 200px;
    }

    .btn-whatsapp {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      background: var(--whatsapp-green);
      color: #061e0e;
      font-weight: 700;
      font-size: 0.95rem;
      padding: 0.85rem 1.35rem;
      border-radius: 0.85rem;
      text-decoration: none;
      box-shadow: 0 4px 16px var(--whatsapp-glow);
      transition: all 0.2s ease;
      cursor: pointer;
      border: none;
    }

    .btn-whatsapp:hover {
      background: var(--whatsapp-hover);
      transform: scale(1.03);
    }

    .btn-copy {
      background: rgba(14, 165, 233, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(14, 165, 233, 0.3);
      padding: 0.55rem;
      border-radius: 0.65rem;
      font-size: 0.85rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
    }

    .btn-copy:hover {
      background: rgba(14, 165, 233, 0.25);
      color: #fff;
    }

    .btn-mark {
      background: rgba(255, 255, 255, 0.05);
      color: var(--muted);
      border: 1px solid var(--card-border);
      padding: 0.55rem;
      border-radius: 0.65rem;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .btn-mark:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }

    .btn-mark.active {
      background: rgba(16, 185, 129, 0.2);
      color: var(--success);
      border-color: rgba(16, 185, 129, 0.4);
    }

    @media (max-width: 768px) {
      .lead-card {
        grid-template-columns: 1fr;
      }
      .lead-actions {
        flex-direction: row;
        flex-wrap: wrap;
      }
      .btn-whatsapp, .btn-copy, .btn-mark {
        flex: 1 1 100%;
      }
    }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div class="badge-user">🦷 Prospecção Ativa • Leonardo</div>
      <h1>Painel de Leads • Clínicas Odontológicas</h1>
      <p class="subtitle">Contatos de consultórios e clínicas odontológicas com WhatsApp direto verificado, sem site cadastrado e com alta reputação no Google Maps.</p>
    </header>

    <div class="stats-grid">
      <div class="stat-card">
        <span class="stat-label">Meta Diária Segura</span>
        <span class="stat-value blue" id="meta-count">25 - 30 Envios</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Mensagens Enviadas</span>
        <span class="stat-value green" id="sent-count">0</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Pendentes na Fila</span>
        <span class="stat-value cyan" id="pending-count">25</span>
      </div>
    </div>

    <div class="safety-box">
      <span class="icon">🛡️</span>
      <div>
        <h4>Cadência Recomendada (Proteção do seu WhatsApp)</h4>
        <p>
          Envie para <strong>25 a 30 contatos por dia</strong>, aguardando de <strong>30 a 60 segundos</strong> entre cada mensagem. O WhatsApp reconhece como envio 100% manual e orgânico!
        </p>
      </div>
    </div>

    <div class="controls-bar">
      <div class="tabs">
        <button class="tab-btn active" onclick="setLimit(15)">🎯 Top 15 Mais Populares</button>
        <button class="tab-btn" onclick="setLimit(30)">🔥 Top 30 Recomendados</button>
        <button class="tab-btn" onclick="setLimit(50)">📋 Todos os 50</button>
      </div>
      <input type="text" class="search-input" id="search-input" placeholder="🔍 Filtrar por nome ou cidade..." oninput="renderLeads()">
    </div>

    <div class="leads-list" id="leads-container"></div>
  </div>

  <script>
    const LEADS_DATA = """ + json.dumps(leads, ensure_ascii=False) + """;

    let currentLimit = 15;
    let sentLeads = JSON.parse(localStorage.getItem('sent_odonto_leads') || '[]');

    function saveSentState() {
      localStorage.setItem('sent_odonto_leads', JSON.stringify(sentLeads));
      updateStats();
    }

    function toggleSent(leadName) {
      if (sentLeads.includes(leadName)) {
        sentLeads = sentLeads.filter(name => name !== leadName);
      } else {
        sentLeads.push(leadName);
      }
      saveSentState();
      renderLeads();
    }

    function updateStats() {
      const visibleLeads = getFilteredLeads();
      const sentCount = visibleLeads.filter(lead => sentLeads.includes(lead.name)).length;
      document.getElementById('sent-count').textContent = sentCount;
      document.getElementById('pending-count').textContent = visibleLeads.length - sentCount;
    }

    function setLimit(limit) {
      currentLimit = limit;
      document.querySelectorAll('.tab-btn').forEach((btn, idx) => {
        btn.classList.remove('active');
        if ((limit === 15 && idx === 0) || (limit === 30 && idx === 1) || (limit === 50 && idx === 2)) {
          btn.classList.add('active');
        }
      });
      renderLeads();
    }

    function getFilteredLeads() {
      const query = document.getElementById('search-input')?.value.toLowerCase().trim() || '';
      let list = LEADS_DATA;
      if (query) {
        list = list.filter(l => 
          l.name.toLowerCase().includes(query) || 
          l.city_state.toLowerCase().includes(query) ||
          l.bairro.toLowerCase().includes(query) ||
          l.whatsapp.includes(query)
        );
      }
      return list.slice(0, currentLimit);
    }

    function copyLeadMessage(index, btn) {
      const visible = getFilteredLeads();
      const lead = visible[index];
      if (!lead) return;
      navigator.clipboard.writeText(lead.mensagem_personalizada).then(() => {
        const originalText = btn.innerHTML;
        btn.innerHTML = '✅ Copiado!';
        setTimeout(() => {
          btn.innerHTML = originalText;
        }, 1500);
      });
    }

    function renderLeads() {
      const container = document.getElementById('leads-container');
      container.innerHTML = '';

      const list = getFilteredLeads();

      if (list.length === 0) {
        container.innerHTML = '<div style="text-align: center; color: var(--muted); padding: 3rem;">Nenhuma clínica encontrada para a busca.</div>';
        updateStats();
        return;
      }

      list.forEach((lead, index) => {
        const isSent = sentLeads.includes(lead.name);
        const card = document.createElement('div');
        card.className = `lead-card ${isSent ? 'sent' : ''}`;

        const safeName = lead.name.replace(/'/g, "\\'");

        card.innerHTML = `
          <div class="lead-info">
            <div class="lead-header">
              <span class="lead-number">#${String(index + 1).padStart(2, '0')}</span>
              <span class="lead-name">${lead.name}</span>
              <span class="rating-badge">★ ${lead.rating} (${lead.reviews} avaliações)</span>
            </div>
            <div class="lead-details">
              <div class="detail-item"><strong>WhatsApp:</strong> ${lead.whatsapp}</div>
              <div class="detail-item"><strong>Localização:</strong> ${lead.bairro} • ${lead.city_state}</div>
              <div class="detail-item"><strong>Categorias:</strong> ${lead.categories}</div>
            </div>
            <div class="msg-preview">${lead.mensagem_personalizada}</div>
          </div>
          <div class="lead-actions">
            <a href="${lead.wa_link_com_mensagem}" target="_blank" class="btn-whatsapp" onclick="if(!sentLeads.includes('${safeName}')) toggleSent('${safeName}')">
              <span>⚡ Abrir WhatsApp</span>
            </a>
            <button class="btn-copy" onclick="copyLeadMessage(${index}, this)">
              📋 Copiar Mensagem
            </button>
            <button class="btn-mark ${isSent ? 'active' : ''}" onclick="toggleSent('${safeName}')">
              ${isSent ? '✓ Mensagem Enviada' : 'Marcar como Enviado'}
            </button>
          </div>
        `;

        container.appendChild(card);
      });

      updateStats();
    }

    // Initial render
    renderLeads();
  </script>
</body>
</html>
"""

with open("disparador_odontologia.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Painel disparador_odontologia.html gerado com sucesso!")
