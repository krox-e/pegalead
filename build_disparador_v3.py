import json
from urllib.parse import quote

with open("clinicas_odontologicas_global.json", "r", encoding="utf-8") as f:
    all_leads = json.load(f)

br_leads = [l for l in all_leads if l.get("country") == "BR"]
pt_leads = [l for l in all_leads if l.get("country") == "PT"]

html_content = f"""<!DOCTYPE html>
<html lang="pt" id="html-root">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel de Prospecção Internacional • Brasil 🇧🇷 & Portugal 🇵🇹</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
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
      --gold: #f59e0b;
      --pt-red: #ef4444;
      --pt-green: #10b981;
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
        radial-gradient(circle at 12% 15%, rgba(14, 165, 233, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 88% 85%, rgba(37, 211, 102, 0.06) 0%, transparent 40%);
      color: var(--text);
      min-height: 100vh;
      padding: 2.5rem 1.5rem;
    }}

    .container {{
      max-width: 1140px;
      margin: 0 auto;
    }}

    header {{
      text-align: center;
      margin-bottom: 2rem;
    }}

    .badge-user {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(14, 165, 233, 0.12);
      border: 1px solid rgba(14, 165, 233, 0.3);
      color: #38bdf8;
      padding: 0.45rem 1.1rem;
      border-radius: 9999px;
      font-size: 0.9rem;
      font-weight: 700;
      margin-bottom: 1rem;
      box-shadow: 0 0 15px rgba(14, 165, 233, 0.15);
    }}

    h1 {{
      font-family: 'Outfit', sans-serif;
      font-size: 2.5rem;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 0%, #bae6fd 50%, #7dd3fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }}

    p.subtitle {{
      color: var(--muted);
      font-size: 1.05rem;
      max-width: 780px;
      margin: 0 auto;
      line-height: 1.5;
    }}

    /* Country Switcher Bar */
    .country-bar {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 0.75rem;
      margin: 2rem 0 1.25rem;
      flex-wrap: wrap;
    }}

    .country-btn {{
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--card-border);
      color: var(--muted);
      padding: 0.75rem 1.5rem;
      border-radius: 0.9rem;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.6rem;
      transition: all 0.25s ease;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}

    .country-btn:hover {{
      border-color: rgba(14, 165, 233, 0.5);
      color: #fff;
      transform: translateY(-2px);
    }}

    .country-btn.active {{
      background: linear-gradient(135deg, rgba(14, 165, 233, 0.25) 0%, rgba(37, 211, 102, 0.2) 100%);
      border-color: #38bdf8;
      color: #ffffff;
      box-shadow: 0 0 20px rgba(14, 165, 233, 0.3);
    }}

    .country-btn .badge-count {{
      background: rgba(255, 255, 255, 0.12);
      padding: 0.2rem 0.6rem;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 800;
    }}

    /* Active Message Template Editor Box */
    .msg-template-box {{
      background: linear-gradient(135deg, rgba(14, 165, 233, 0.08) 0%, rgba(37, 211, 102, 0.06) 100%);
      border: 1px solid rgba(14, 165, 233, 0.3);
      border-radius: 1.1rem;
      padding: 1.25rem 1.5rem;
      margin-bottom: 2rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }}

    .msg-template-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.5rem;
    }}

    .msg-template-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.05rem;
      font-weight: 700;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .msg-template-tag {{
      background: rgba(14, 165, 233, 0.2);
      color: #7dd3fc;
      padding: 0.2rem 0.6rem;
      border-radius: 0.4rem;
      font-size: 0.78rem;
      font-weight: 700;
    }}

    .msg-template-input {{
      background: rgba(11, 17, 32, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 0.75rem;
      padding: 0.75rem 1rem;
      color: #fff;
      font-size: 0.95rem;
      font-family: inherit;
      line-height: 1.45;
      width: 100%;
      resize: vertical;
      min-height: 55px;
      outline: none;
      transition: all 0.2s;
    }}

    .msg-template-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 10px var(--primary-glow);
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

    .stat-value.blue {{ color: #38bdf8; }}
    .stat-value.green {{ color: var(--whatsapp-green); }}
    .stat-value.cyan {{ color: #22d3ee; }}
    .stat-value.gold {{ color: var(--gold); }}

    /* Safety Box */
    .safety-box {{
      background: rgba(14, 165, 233, 0.08);
      border: 1px solid rgba(14, 165, 233, 0.3);
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
      color: #38bdf8;
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
      color: #ffffff;
      box-shadow: 0 0 12px var(--primary-glow);
    }}

    .search-input {{
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--card-border);
      border-radius: 0.85rem;
      padding: 0.65rem 1.2rem;
      color: #fff;
      font-size: 0.95rem;
      outline: none;
      min-width: 290px;
    }}

    .search-input:focus {{
      border-color: var(--primary);
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
      border-color: rgba(14, 165, 233, 0.4);
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
      gap: 0.65rem;
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

    .country-pill {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.2rem 0.65rem;
      border-radius: 0.5rem;
      font-size: 0.8rem;
      font-weight: 700;
    }}

    .country-pill.br {{
      background: rgba(37, 211, 102, 0.12);
      color: #4ade80;
      border: 1px solid rgba(37, 211, 102, 0.3);
    }}

    .country-pill.pt {{
      background: rgba(239, 68, 68, 0.12);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}

    .lead-name {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.25rem;
      font-weight: 700;
      color: #ffffff;
    }}

    .rating-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      background: rgba(255, 184, 77, 0.12);
      color: #ffb84d;
      padding: 0.25rem 0.6rem;
      border-radius: 0.5rem;
      font-size: 0.85rem;
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

    .detail-item .phone-val {{
      font-family: 'JetBrains Mono', monospace;
      color: #38bdf8;
      font-weight: 700;
    }}

    .msg-box-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.75rem;
      color: var(--muted);
      margin-top: 0.4rem;
      font-weight: 600;
    }}

    .msg-preview {{
      background: rgba(11, 17, 32, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 0.75rem;
      padding: 0.85rem 1.1rem;
      font-size: 0.875rem;
      color: #e2e8f0;
      line-height: 1.5;
      margin-top: 0.25rem;
      white-space: pre-line;
      max-height: 130px;
      overflow-y: auto;
    }}

    /* Actions */
    .lead-actions {{
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      min-width: 210px;
    }}

    .btn-whatsapp {{
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
    }}

    .btn-whatsapp:hover {{
      background: var(--whatsapp-hover);
      transform: scale(1.03);
    }}

    .btn-copy {{
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
    }}

    .btn-copy:hover {{
      background: rgba(14, 165, 233, 0.25);
      color: #fff;
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
        flex-wrap: wrap;
      }}
      .btn-whatsapp, .btn-copy, .btn-mark {{
        flex: 1 1 100%;
      }}
    }}
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div class="badge-user" id="header-badge">🌍 Prospecção Internacional • Leonardo</div>
      <h1 id="header-title">Painel de Leads • Clínicas Odontológicas & Dentárias</h1>
      <p class="subtitle" id="header-subtitle">Contatos e contactos de consultórios e clínicas no <strong>Brasil 🇧🇷</strong> e <strong>Portugal 🇵🇹</strong> com WhatsApp direto verificado, sem website e com excelente reputação no Google Maps.</p>
    </header>

    <!-- Country Selector -->
    <div class="country-bar">
      <button class="country-btn" id="btn-country-pt" onclick="setCountry('PT')">
        <span>🇵🇹 Portugal</span>
        <span class="badge-count" id="count-pt">{len(pt_leads)}</span>
      </button>
      <button class="country-btn active" id="btn-country-br" onclick="setCountry('BR')">
        <span>🇧🇷 Brasil</span>
        <span class="badge-count" id="count-br">{len(br_leads)}</span>
      </button>
      <button class="country-btn" id="btn-country-all" onclick="setCountry('ALL')">
        <span>🌐 Todos os Países</span>
        <span class="badge-count" id="count-all">{len(all_leads)}</span>
      </button>
    </div>

    <!-- Active Message Template Editor Box -->
    <div class="msg-template-box">
      <div class="msg-template-header">
        <div class="msg-template-title">
          <span>💬 Mensagem Ativa de Prospecção</span>
          <span class="msg-template-tag" id="msg-lang-badge">🇧🇷 Português do Brasil (PT-BR)</span>
        </div>
        <button onclick="restoreDefaultMessage()" style="background: transparent; border: 1px solid rgba(255,255,255,0.15); color: var(--muted); font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 0.4rem; cursor: pointer;">
          ↺ Restaurar Mensagem Padrão
        </button>
      </div>
      <textarea id="active-msg-input" class="msg-template-input" oninput="onCustomMessageChange(this.value)">Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta.</textarea>
      <small style="color: var(--muted); font-size: 0.75rem;">Esta mensagem é incorporada automaticamente em todos os botões <strong>⚡ Abrir WhatsApp</strong> e <strong>📋 Copiar</strong> da lista abaixo.</small>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <span class="stat-label" id="lbl-meta">Meta Diária Segura</span>
        <span class="stat-value blue" id="meta-count">25 - 30 Envios</span>
      </div>
      <div class="stat-card">
        <span class="stat-label" id="lbl-sent">Mensagens Enviadas</span>
        <span class="stat-value green" id="sent-count">0</span>
      </div>
      <div class="stat-card">
        <span class="stat-label" id="lbl-pending">Pendentes na Fila</span>
        <span class="stat-value cyan" id="pending-count">0</span>
      </div>
      <div class="stat-card">
        <span class="stat-label" id="lbl-total">Total Disponível</span>
        <span class="stat-value gold" id="total-available">{len(br_leads)}</span>
      </div>
    </div>

    <div class="safety-box">
      <span class="icon">🛡️</span>
      <div>
        <h4 id="safety-title">Cadência Internacional Recomendada (Proteção do seu WhatsApp)</h4>
        <p id="safety-text">
          Envie para <strong>25 a 30 contactos por dia</strong>, aguardando de <strong>30 a 60 segundos</strong> entre cada mensagem. O WhatsApp reconhece como envio 100% manual e orgânico para telemóveis de Portugal (+351) e do Brasil (+55)!
        </p>
      </div>
    </div>

    <div class="controls-bar">
      <div class="tabs">
        <button class="tab-btn" onclick="setLimit(15)" id="btn-top15">🎯 Top 15</button>
        <button class="tab-btn" onclick="setLimit(30)" id="btn-top30">🔥 Top 30 Recomendados</button>
        <button class="tab-btn active" onclick="setLimit(100)" id="btn-all">📋 Todos</button>
      </div>
      <input type="text" class="search-input" id="search-input" placeholder="🔍 Filtrar por nome, cidade (ex: Lisboa, Porto, SP, RJ)..." oninput="renderLeads()">
    </div>

    <div class="leads-list" id="leads-container"></div>
  </div>

  <script>
    const LEADS_DATA = {json.dumps(all_leads, ensure_ascii=False)};

    const DEFAULT_MSG_PT = "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para a vossa clínica.";
    const DEFAULT_MSG_BR = "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta.";

    let currentCountry = 'BR'; // 'BR' | 'PT' | 'ALL'
    let currentLimit = 100;
    let sentLeads = JSON.parse(localStorage.getItem('sent_odonto_leads') || '[]');

    let customMsgPT = DEFAULT_MSG_PT;
    let customMsgBR = DEFAULT_MSG_BR;

    function saveSentState() {{
      localStorage.setItem('sent_odonto_leads', JSON.stringify(sentLeads));
      updateStats();
    }}

    function toggleSent(leadName) {{
      if (sentLeads.includes(leadName)) {{
        sentLeads = sentLeads.filter(name => name !== leadName);
      }} else {{
        sentLeads.push(leadName);
      }}
      saveSentState();
      renderLeads();
    }}

    function onCustomMessageChange(val) {{
      if (currentCountry === 'PT') {{
        customMsgPT = val;
      }} else {{
        customMsgBR = val;
      }}
      renderLeads();
    }}

    function restoreDefaultMessage() {{
      if (currentCountry === 'PT') {{
        customMsgPT = DEFAULT_MSG_PT;
        document.getElementById('active-msg-input').value = DEFAULT_MSG_PT;
      }} else {{
        customMsgBR = DEFAULT_MSG_BR;
        document.getElementById('active-msg-input').value = DEFAULT_MSG_BR;
      }}
      renderLeads();
    }}

    function setCountry(country) {{
      currentCountry = country;
      document.getElementById('btn-country-all').classList.toggle('active', country === 'ALL');
      document.getElementById('btn-country-br').classList.toggle('active', country === 'BR');
      document.getElementById('btn-country-pt').classList.toggle('active', country === 'PT');

      const headerSubtitle = document.getElementById('header-subtitle');
      const headerTitle = document.getElementById('header-title');
      const msgLangBadge = document.getElementById('msg-lang-badge');
      const activeMsgInput = document.getElementById('active-msg-input');

      if (country === 'PT') {{
        document.documentElement.lang = 'pt-PT';
        headerTitle.textContent = 'Painel de Leads • Clínicas Dentárias & Médicos Dentistas';
        headerSubtitle.innerHTML = 'Contactos de consultórios e clínicas dentárias em <strong>Portugal 🇵🇹</strong> com telemóvel WhatsApp direto verificado, sem website e com excelente reputação no Google Maps.';
        msgLangBadge.innerHTML = '🇵🇹 Português de Portugal (PT-PT)';
        activeMsgInput.value = customMsgPT;
      }} else if (country === 'BR') {{
        document.documentElement.lang = 'pt-BR';
        headerTitle.textContent = 'Painel de Leads • Clínicas Odontológicas';
        headerSubtitle.innerHTML = 'Contatos de consultórios e clínicas odontológicas no <strong>Brasil 🇧🇷</strong> com WhatsApp direto verificado, sem site cadastrado e com alta reputação no Google Maps.';
        msgLangBadge.innerHTML = '🇧🇷 Português do Brasil (PT-BR)';
        activeMsgInput.value = customMsgBR;
      }} else {{
        document.documentElement.lang = 'pt';
        headerTitle.textContent = 'Painel de Leads • Clínicas Odontológicas & Dentárias';
        headerSubtitle.innerHTML = 'Contatos e contactos de consultórios e clínicas no <strong>Brasil 🇧🇷</strong> e <strong>Portugal 🇵🇹</strong> com WhatsApp direto verificado e sem site cadastrado.';
        msgLangBadge.innerHTML = '🌐 Modo Internacional (PT-PT & PT-BR)';
        activeMsgInput.value = customMsgPT;
      }}

      renderLeads();
    }}

    function setLimit(limit) {{
      currentLimit = limit;
      document.querySelectorAll('.tab-btn').forEach((btn, idx) => {{
        btn.classList.remove('active');
        if ((limit === 15 && idx === 0) || (limit === 30 && idx === 1) || (limit === 100 && idx === 2)) {{
          btn.classList.add('active');
        }}
      }});
      renderLeads();
    }}

    function getFilteredLeads() {{
      const query = document.getElementById('search-input')?.value.toLowerCase().trim() || '';
      let list = LEADS_DATA;

      if (currentCountry !== 'ALL') {{
        list = list.filter(l => l.country === currentCountry);
      }}

      if (query) {{
        list = list.filter(l => 
          l.name.toLowerCase().includes(query) || 
          (l.city_state && l.city_state.toLowerCase().includes(query)) ||
          (l.bairro && l.bairro.toLowerCase().includes(query)) ||
          (l.whatsapp && l.whatsapp.includes(query)) ||
          (l.country_label && l.country_label.toLowerCase().includes(query))
        );
      }}
      return list.slice(0, currentLimit);
    }}

    function updateStats() {{
      const visibleLeads = getFilteredLeads();
      const sentCount = visibleLeads.filter(lead => sentLeads.includes(lead.name)).length;
      document.getElementById('sent-count').textContent = sentCount;
      document.getElementById('pending-count').textContent = visibleLeads.length - sentCount;
      document.getElementById('total-available').textContent = visibleLeads.length;
    }}

    function getLeadEffectiveMessage(lead) {{
      if (lead.country === 'PT') {{
        return customMsgPT;
      }}
      return customMsgBR;
    }}

    function copyLeadMessage(leadIndex, btn) {{
      const visible = getFilteredLeads();
      const lead = visible[leadIndex];
      if (!lead) return;
      const msg = getLeadEffectiveMessage(lead);
      navigator.clipboard.writeText(msg).then(() => {{
        const originalText = btn.innerHTML;
        btn.innerHTML = '✅ Copiado!';
        setTimeout(() => {{
          btn.innerHTML = originalText;
        }}, 1500);
      }});
    }}

    function renderLeads() {{
      const container = document.getElementById('leads-container');
      container.innerHTML = '';

      const list = getFilteredLeads();

      if (list.length === 0) {{
        container.innerHTML = '<div style="text-align: center; color: var(--muted); padding: 3rem;">Nenhum estabelecimento encontrado para este filtro.</div>';
        updateStats();
        return;
      }}

      list.forEach((lead, index) => {{
        const isSent = sentLeads.includes(lead.name);
        const card = document.createElement('div');
        card.className = `lead-card ${{isSent ? 'sent' : ''}}`;

        const safeName = lead.name.replace(/'/g, "\\'");
        const isPt = lead.country === 'PT';
        const phoneLabel = isPt ? 'Telemóvel' : 'WhatsApp';
        const locLabel = isPt ? 'Localização' : 'Localização';
        const langBadge = isPt ? '🇵🇹 Português de Portugal' : '🇧🇷 Português do Brasil';
        
        const effectiveMsg = getLeadEffectiveMessage(lead);
        const waLinkWithMsg = `${{lead.wa_link}}?text=${{encodeURIComponent(effectiveMsg)}}`;

        card.innerHTML = `
          <div class="lead-info">
            <div class="lead-header">
              <span class="lead-number">#${{String(index + 1).padStart(2, '0')}}</span>
              <span class="country-pill ${{isPt ? 'pt' : 'br'}}">
                ${{lead.flag || (isPt ? '🇵🇹' : '🇧🇷')}} ${{lead.country_label || (isPt ? 'Portugal' : 'Brasil')}}
              </span>
              <span class="lead-name">${{lead.name}}</span>
              <span class="rating-badge">★ ${{lead.rating}} (${{lead.reviews}} avaliações)</span>
            </div>
            <div class="lead-details">
              <div class="detail-item"><strong>${{phoneLabel}}:</strong> <span class="phone-val">${{lead.whatsapp}}</span></div>
              <div class="detail-item"><strong>${{locLabel}}:</strong> ${{lead.bairro ? lead.bairro + ' • ' : ''}}${{lead.city_state}}</div>
              <div class="detail-item"><strong>Categorias:</strong> ${{lead.categories}}</div>
            </div>
            <div class="msg-box-header">
              <span>Mensagem de Prospecção</span>
              <span style="color: var(--accent); font-weight: 700;">${{langBadge}}</span>
            </div>
            <div class="msg-preview">${{effectiveMsg}}</div>
          </div>
          <div class="lead-actions">
            <a href="${{waLinkWithMsg}}" target="_blank" class="btn-whatsapp" onclick="if(!sentLeads.includes('${{safeName}}')) toggleSent('${{safeName}}')">
              <span>⚡ Abrir WhatsApp</span>
            </a>
            <button class="btn-copy" onclick="copyLeadMessage(${{index}}, this)">
              📋 Copiar Mensagem
            </button>
            <button class="btn-mark ${{isSent ? 'active' : ''}}" onclick="toggleSent('${{safeName}}')">
              ${{isSent ? '✓ Mensagem Enviada' : 'Marcar como Enviado'}}
            </button>
          </div>
        `;

        container.appendChild(card);
      }});

      updateStats();
    }}

    // Initial render in Brazil mode
    setCountry('BR');
  </script>
</body>
</html>
"""

with open("disparador_whatsapp.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("disparador_whatsapp.html e index.html gerados com sucesso!")
