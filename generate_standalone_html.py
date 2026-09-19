import json

with open("churrascarias_sem_site_100.json", "r", encoding="utf-8") as f:
    leads = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel de Disparo WhatsApp • Leonardo</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0b0f19;
      --card-bg: rgba(22, 30, 49, 0.85);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #25d366;
      --primary-hover: #1ebd5b;
      --primary-glow: rgba(37, 211, 102, 0.25);
      --accent: #ff9900;
      --text: #f3f4f6;
      --muted: #9ca3af;
      --success: #10b981;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Inter', sans-serif;
      background-color: var(--bg);
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(37, 211, 102, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(255, 153, 0, 0.06) 0%, transparent 40%);
      color: var(--text);
      min-height: 100vh;
      padding: 2.5rem 1.5rem;
    }}

    .container {{
      max-width: 1100px;
      margin: 0 auto;
    }}

    header {{
      text-align: center;
      margin-bottom: 2.5rem;
    }}

    .badge-user {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(37, 211, 102, 0.12);
      border: 1px solid rgba(37, 211, 102, 0.3);
      color: var(--primary);
      padding: 0.4rem 1rem;
      border-radius: 9999px;
      font-size: 0.9rem;
      font-weight: 700;
      margin-bottom: 1rem;
      box-shadow: 0 0 15px rgba(37, 211, 102, 0.15);
    }}

    h1 {{
      font-family: 'Outfit', sans-serif;
      font-size: 2.5rem;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }}

    p.subtitle {{
      color: var(--muted);
      font-size: 1.1rem;
      max-width: 650px;
      margin: 0 auto;
    }}

    /* Stats Grid */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }}

    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 1.1rem;
      padding: 1.35rem;
      backdrop-filter: blur(12px);
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }}

    .stat-label {{
      font-size: 0.825rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 700;
    }}

    .stat-value {{
      font-family: 'Outfit', sans-serif;
      font-size: 2rem;
      font-weight: 800;
      color: #fff;
    }}

    .stat-value.green {{ color: var(--primary); }}
    .stat-value.orange {{ color: var(--accent); }}

    /* Safety Box */
    .safety-box {{
      background: rgba(255, 153, 0, 0.08);
      border: 1px solid rgba(255, 153, 0, 0.3);
      border-radius: 1.1rem;
      padding: 1.25rem 1.5rem;
      margin-bottom: 2rem;
      display: flex;
      align-items: center;
      gap: 1.25rem;
    }}

    .safety-box span.icon {{
      font-size: 2rem;
    }}

    .safety-box h4 {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.1rem;
      color: var(--accent);
      margin-bottom: 0.25rem;
    }}

    .safety-box p {{
      font-size: 0.925rem;
      color: #e5e7eb;
      line-height: 1.45;
    }}

    /* Controls Bar */
    .controls-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1.5rem;
    }}

    .tabs {{
      display: flex;
      background: rgba(15, 23, 42, 0.9);
      padding: 0.4rem;
      border-radius: 0.85rem;
      border: 1px solid var(--card-border);
      gap: 0.4rem;
    }}

    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--muted);
      padding: 0.6rem 1.2rem;
      border-radius: 0.6rem;
      font-size: 0.925rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .tab-btn.active {{
      background: var(--primary);
      color: #0b0f19;
      box-shadow: 0 0 12px var(--primary-glow);
    }}

    /* Leads List */
    .leads-list {{
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }}

    .lead-card {{
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
    }}

    .lead-card:hover {{
      border-color: rgba(37, 211, 102, 0.4);
      transform: translateY(-2px);
    }}

    .lead-card.sent {{
      border-color: rgba(16, 185, 129, 0.35);
      background: rgba(16, 185, 129, 0.06);
    }}

    .lead-info {{
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }}

    .lead-header {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      flex-wrap: wrap;
    }}

    .lead-number {{
      font-size: 0.85rem;
      font-weight: 800;
      background: rgba(255, 255, 255, 0.08);
      padding: 0.25rem 0.65rem;
      border-radius: 0.5rem;
      color: var(--muted);
    }}

    .lead-name {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.3rem;
      font-weight: 700;
      color: #ffffff;
    }}

    .rating-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      background: rgba(255, 153, 0, 0.12);
      color: #ffb84d;
      padding: 0.25rem 0.6rem;
      border-radius: 0.5rem;
      font-size: 0.875rem;
      font-weight: 700;
    }}

    .lead-details {{
      display: flex;
      flex-wrap: wrap;
      gap: 1.25rem;
      font-size: 0.9rem;
      color: var(--muted);
    }}

    .detail-item {{
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }}

    .detail-item strong {{
      color: #e5e7eb;
    }}

    .msg-preview {{
      background: rgba(11, 15, 25, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 0.75rem;
      padding: 0.85rem 1.1rem;
      font-size: 0.875rem;
      color: #e2e8f0;
      line-height: 1.5;
      margin-top: 0.35rem;
      white-space: pre-line;
      max-height: 100px;
      overflow-y: auto;
    }}

    /* Actions */
    .lead-actions {{
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      min-width: 190px;
    }}

    .btn-whatsapp {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      background: var(--primary);
      color: #061e0e;
      font-weight: 700;
      font-size: 0.95rem;
      padding: 0.85rem 1.35rem;
      border-radius: 0.85rem;
      text-decoration: none;
      box-shadow: 0 4px 16px var(--primary-glow);
      transition: all 0.2s ease;
      cursor: pointer;
      border: none;
    }}

    .btn-whatsapp:hover {{
      background: var(--primary-hover);
      transform: scale(1.03);
    }}

    .btn-mark {{
      background: rgba(255, 255, 255, 0.05);
      color: var(--muted);
      border: 1px solid var(--card-border);
      padding: 0.55rem;
      border-radius: 0.65rem;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .btn-mark:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }}

    .btn-mark.active {{
      background: rgba(16, 185, 129, 0.2);
      color: var(--success);
      border-color: rgba(16, 185, 129, 0.4);
    }}

    @media (max-width: 768px) {{
      .lead-card {{
        grid-template-columns: 1fr;
      }}
      .lead-actions {{
        flex-direction: row;
      }}
    }}
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div class="badge-user">⚡ Painel de Disparo WhatsApp • Leonardo</div>
      <h1>Prospecção Direta para Churrascarias</h1>
      <p class="subtitle">Clique no botão para abrir a conversa no WhatsApp com a mensagem personalizada pronta para envio.</p>
    </header>

    <div class="stats-grid">
      <div class="stat-card">
        <span class="stat-label">Meta Recomendada</span>
        <span class="stat-value orange" id="meta-count">25 - 30 Envios</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Mensagens Enviadas</span>
        <span class="stat-value green" id="sent-count">0</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Pendentes na Fila</span>
        <span class="stat-value" id="pending-count">25</span>
      </div>
    </div>

    <div class="safety-box">
      <span class="icon">🛡️</span>
      <div>
        <h4>Proteção Anti-Bloqueio (Segurança do seu WhatsApp)</h4>
        <p>
          Envie para <strong>25 a 30 contatos por dia</strong>, aguardando de <strong>30 a 60 segundos</strong> entre cada mensagem. O WhatsApp reconhece como envio 100% humano e seguro!
        </p>
      </div>
    </div>

    <div class="controls-bar">
      <div class="tabs">
        <button class="tab-btn active" onclick="setLimit(25)">🎯 Top 25 (Mais Populares)</button>
        <button class="tab-btn" onclick="setLimit(50)">🔥 Top 50</button>
        <button class="tab-btn" onclick="setLimit(100)">📋 Todos os 100</button>
      </div>
      <div style="font-size: 0.925rem; color: var(--muted);">
        Remetente: <strong style="color: #fff;">Leonardo</strong>
      </div>
    </div>

    <div class="leads-list" id="leads-container"></div>
  </div>

  <script>
    // Embedded 100 leads directly to avoid any browser CORS issues
    const LEADS_DATA = {json.dumps(leads, ensure_ascii=False)};

    let currentLimit = 25;
    let sentIds = new Set(JSON.parse(localStorage.getItem('sent_leads_leonardo_v2') || '[]'));

    function setLimit(limit) {{
      currentLimit = limit;
      document.querySelectorAll('.tab-btn').forEach((btn, idx) => {{
        if ((limit === 25 && idx === 0) || (limit === 50 && idx === 1) || (limit === 100 && idx === 2)) {{
          btn.classList.add('active');
        }} else {{
          btn.classList.remove('active');
        }}
      }});
      renderLeads();
    }}

    function toggleSent(index) {{
      if (sentIds.has(index)) {{
        sentIds.delete(index);
      }} else {{
        sentIds.add(index);
      }}
      localStorage.setItem('sent_leads_leonardo_v2', JSON.stringify(Array.from(sentIds)));
      renderLeads();
    }}

    function openWhatsApp(url, index) {{
      window.open(url, '_blank');
      if (!sentIds.has(index)) {{
        sentIds.add(index);
        localStorage.setItem('sent_leads_leonardo_v2', JSON.stringify(Array.from(sentIds)));
        renderLeads();
      }}
    }}

    function renderLeads() {{
      const container = document.getElementById('leads-container');
      const leadsToRender = LEADS_DATA.slice(0, currentLimit);
      
      let sentTotal = 0;
      leadsToRender.forEach((_, idx) => {{
        if (sentIds.has(idx)) sentTotal++;
      }});

      document.getElementById('sent-count').textContent = sentTotal;
      document.getElementById('pending-count').textContent = leadsToRender.length - sentTotal;

      container.innerHTML = leadsToRender.map((lead, idx) => {{
        const isSent = sentIds.has(idx);
        return `
          <div class="lead-card ${{isSent ? 'sent' : ''}}">
            <div class="lead-info">
              <div class="lead-header">
                <span class="lead-number">#${{String(idx + 1).padStart(2, '0')}}</span>
                <span class="lead-name">${{lead.name}}</span>
                <span class="rating-badge">★ ${{lead.rating}} (${{lead.reviews}} avaliações)</span>
              </div>
              <div class="lead-details">
                <div class="detail-item">📱 <strong>${{lead.whatsapp}}</strong></div>
                <div class="detail-item">📍 ${{lead.bairro}} &bull; ${{lead.city_state}}</div>
              </div>
              <div class="msg-preview">${{lead.mensagem_personalizada}}</div>
            </div>
            <div class="lead-actions">
              <button class="btn-whatsapp" onclick="openWhatsApp('${{lead.wa_link_com_mensagem}}', ${{idx}})">
                🚀 Enviar WhatsApp
              </button>
              <button class="btn-mark ${{isSent ? 'active' : ''}}" onclick="toggleSent(${{idx}})">
                ${{isSent ? '✔ Enviado' : 'Marcar como Enviado'}}
              </button>
            </div>
          </div>
        `;
      }}).join('');
    }}

    renderLeads();
  </script>
</body>
</html>
"""

with open("disparador_whatsapp.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Painel HTML atualizado com dados embutidos com sucesso!")
