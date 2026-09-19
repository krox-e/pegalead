import json
from urllib.parse import quote

with open("clinicas_odontologicas_global.json", "r", encoding="utf-8") as f:
    all_leads = json.load(f)

br_leads = [l for l in all_leads if l.get("country") == "BR"]
pt_leads = [l for l in all_leads if l.get("country") == "PT"]

html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Painel de Prospecção • Clínicas Odontológicas</title>
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
      --danger: #ef4444;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      overflow-x: hidden;
      width: 100%;
      max-width: 100vw;
    }}

    body {{
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      background-color: var(--bg);
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(14, 165, 233, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(56, 189, 248, 0.06) 0%, transparent 40%);
      color: var(--text);
      min-height: 100vh;
      padding: 2.5rem 1.5rem;
    }}

    .container {{
      max-width: 1100px;
      margin: 0 auto;
      width: 100%;
    }}

    header {{
      text-align: center;
      margin-bottom: 2.5rem;
    }}

    .badge-user {{
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
      font-size: 1.1rem;
      max-width: 700px;
      margin: 0 auto;
      line-height: 1.5;
    }}

    /* Country Pills Bar */
    .country-pills-bar {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 0.6rem;
      margin-top: 1.5rem;
      flex-wrap: wrap;
    }}

    .country-pill-btn {{
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--card-border);
      color: var(--muted);
      padding: 0.5rem 1.1rem;
      border-radius: 9999px;
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      transition: all 0.2s ease;
    }}

    .country-pill-btn:hover {{
      color: #fff;
      border-color: rgba(14, 165, 233, 0.4);
    }}

    .country-pill-btn.active {{
      background: rgba(14, 165, 233, 0.18);
      border-color: #38bdf8;
      color: #ffffff;
      box-shadow: 0 0 12px rgba(14, 165, 233, 0.25);
    }}

    .country-pill-btn .pill-count {{
      background: rgba(255, 255, 255, 0.1);
      padding: 0.15rem 0.45rem;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 800;
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
      flex-shrink: 0;
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

    /* Bulk Automation Banner */
    .bulk-action-bar {{
      background: linear-gradient(135deg, rgba(37, 211, 102, 0.15) 0%, rgba(14, 165, 233, 0.12) 100%);
      border: 1px solid rgba(37, 211, 102, 0.35);
      border-radius: 1.1rem;
      padding: 1rem 1.5rem;
      margin-bottom: 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}

    .bulk-action-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.1rem;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .btn-bulk-start {{
      background: var(--whatsapp-green);
      color: #061e0e;
      border: none;
      font-weight: 800;
      font-size: 1rem;
      padding: 0.8rem 1.6rem;
      border-radius: 0.85rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.6rem;
      box-shadow: 0 4px 18px var(--whatsapp-glow);
      transition: all 0.2s ease;
    }}

    .btn-bulk-start:hover {{
      background: var(--whatsapp-hover);
      transform: scale(1.03);
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
      padding: 0.6rem 1rem;
      color: #fff;
      font-size: 0.95rem;
      outline: none;
      min-width: 260px;
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
      overflow-wrap: break-word;
      word-break: break-word;
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
      min-width: 0;
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
      flex-shrink: 0;
    }}

    .lead-name {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.3rem;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.3;
    }}

    .rating-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      background: rgba(255, 184, 77, 0.12);
      color: #ffb84d;
      padding: 0.25rem 0.6rem;
      border-radius: 0.5rem;
      font-size: 0.875rem;
      font-weight: 700;
      flex-shrink: 0;
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
    }}

    /* Actions */
    .lead-actions {{
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      min-width: 200px;
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

    /* Automation Modal */
    .modal-backdrop {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(8px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 9999;
      padding: 1rem;
    }}

    .modal-backdrop.open {{
      display: flex;
    }}

    .modal-box {{
      background: #0f172a;
      border: 1px solid rgba(37, 211, 102, 0.4);
      border-radius: 1.4rem;
      max-width: 580px;
      width: 100%;
      padding: 2rem;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(37, 211, 102, 0.2);
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }}

    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .modal-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.4rem;
      font-weight: 800;
      color: #fff;
    }}

    .modal-close {{
      background: transparent;
      border: none;
      color: var(--muted);
      font-size: 1.5rem;
      cursor: pointer;
    }}

    .modal-close:hover {{ color: #fff; }}

    .progress-bar-bg {{
      width: 100%;
      height: 10px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 999px;
      overflow: hidden;
      margin: 0.5rem 0;
    }}

    .progress-bar-fill {{
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #25d366, #38bdf8);
      border-radius: 999px;
      transition: width 0.3s ease;
    }}

    .timer-display {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 2rem;
      font-weight: 800;
      color: #38bdf8;
      text-align: center;
      margin: 0.5rem 0;
    }}

    /* ==========================================================
       SUPER RESPONSIVE MOBILE OPTIMIZATIONS (Smart Compact View)
       ========================================================== */
    @media (max-width: 768px) {{
      body {{
        padding: 1.25rem 0.85rem;
      }}

      header {{
        margin-bottom: 1.25rem;
      }}

      .badge-user {{
        font-size: 0.8rem;
        padding: 0.35rem 0.8rem;
        margin-bottom: 0.6rem;
      }}

      h1 {{
        font-size: 1.6rem;
        margin-bottom: 0.35rem;
      }}

      p.subtitle {{
        font-size: 0.875rem;
        line-height: 1.35;
      }}

      .country-pills-bar {{
        gap: 0.4rem;
        margin-top: 1rem;
      }}

      .country-pill-btn {{
        padding: 0.4rem 0.75rem;
        font-size: 0.8rem;
        gap: 0.35rem;
      }}

      /* Super compact horizontal 3-column stats on mobile */
      .stats-grid {{
        grid-template-columns: repeat(3, 1fr);
        gap: 0.5rem;
        margin-bottom: 1.25rem;
      }}

      .stat-card {{
        padding: 0.75rem 0.4rem;
        border-radius: 0.85rem;
        text-align: center;
        align-items: center;
      }}

      .stat-label {{
        font-size: 0.65rem;
        letter-spacing: 0.02em;
        line-height: 1.2;
      }}

      .stat-value {{
        font-size: 1.25rem;
        margin-top: 0.2rem;
      }}

      /* Bulk Action Banner compact */
      .bulk-action-bar {{
        padding: 0.85rem 1rem;
        margin-bottom: 1rem;
        flex-direction: column;
        align-items: stretch;
        text-align: center;
        gap: 0.6rem;
      }}

      .bulk-action-title {{
        font-size: 0.95rem;
        justify-content: center;
      }}

      .btn-bulk-start {{
        width: 100%;
        justify-content: center;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
      }}

      /* Compact Safety Box */
      .safety-box {{
        padding: 0.85rem 1rem;
        margin-bottom: 1.2rem;
        gap: 0.75rem;
      }}

      .safety-box span.icon {{
        font-size: 1.5rem;
      }}

      .safety-box h4 {{
        font-size: 0.95rem;
        margin-bottom: 0.15rem;
      }}

      .safety-box p {{
        font-size: 0.8rem;
        line-height: 1.35;
      }}

      /* Controls & Search */
      .controls-bar {{
        flex-direction: column;
        align-items: stretch;
        gap: 0.65rem;
        margin-bottom: 1rem;
      }}

      .tabs {{
        width: 100%;
        display: grid;
        grid-template-columns: 1fr 1.3fr 1fr;
        gap: 0.25rem;
        padding: 0.3rem;
      }}

      .tab-btn {{
        padding: 0.5rem 0.25rem;
        font-size: 0.75rem;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }}

      .search-input {{
        width: 100%;
        min-width: 0;
        padding: 0.65rem 1rem;
        font-size: 0.9rem;
      }}

      /* Super Sleek Lead Cards on Mobile */
      .leads-list {{
        gap: 1rem;
      }}

      .lead-card {{
        grid-template-columns: 1fr;
        padding: 1rem;
        border-radius: 1rem;
        gap: 0.85rem;
      }}

      .lead-header {{
        gap: 0.4rem;
      }}

      .lead-number {{
        font-size: 0.75rem;
        padding: 0.2rem 0.5rem;
      }}

      .lead-name {{
        font-size: 1.1rem;
      }}

      .rating-badge {{
        font-size: 0.75rem;
        padding: 0.2rem 0.5rem;
      }}

      .lead-details {{
        flex-direction: column;
        gap: 0.35rem;
        font-size: 0.825rem;
      }}

      .msg-preview {{
        font-size: 0.8rem;
        padding: 0.65rem 0.85rem;
        line-height: 1.4;
        max-height: 80px;
        margin-top: 0.25rem;
      }}

      /* 2-Row Action Buttons Grid on Mobile */
      .lead-actions {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
        width: 100%;
        min-width: 0;
      }}

      .btn-whatsapp {{
        grid-column: span 2;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
      }}

      .btn-copy, .btn-mark {{
        padding: 0.55rem 0.5rem;
        font-size: 0.8rem;
        text-align: center;
        justify-content: center;
        white-space: nowrap;
      }}

      /* Modal on Mobile */
      .modal-box {{
        padding: 1.25rem;
        border-radius: 1.1rem;
        gap: 1rem;
        max-width: 95vw;
      }}

      .modal-title {{
        font-size: 1.15rem;
      }}
    }}
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div class="badge-user">🦷 Prospecção Ativa • Leonardo</div>
      <h1>Painel de Leads • Clínicas Odontológicas</h1>
      <p class="subtitle">Contatos de consultórios e clínicas odontológicas com WhatsApp direto verificado, sem site cadastrado e com alta reputação no Google Maps.</p>
      
      <!-- Country Pills -->
      <div class="country-pills-bar">
        <button class="country-pill-btn active" id="pill-br" onclick="setCountry('BR')">
          <svg width="18" height="13" viewBox="0 0 720 504" style="border-radius:2px;"><rect width="720" height="504" fill="#009c3b"/><polygon points="360,42 678,252 360,462 42,252" fill="#ffdf00"/><circle cx="360" cy="252" r="126" fill="#002776"/><path d="M 234 252 A 126 126 0 0 0 486 252 A 136 136 0 0 1 234 252" fill="#ffffff"/></svg>
          <span>Brasil</span>
          <span class="pill-count">{len(br_leads)}</span>
        </button>
        <button class="country-pill-btn" id="pill-pt" onclick="setCountry('PT')">
          <svg width="18" height="13" viewBox="0 0 600 400" style="border-radius:2px;"><rect width="240" height="400" fill="#046A38"/><rect x="240" width="360" height="400" fill="#DA291C"/><circle cx="240" cy="200" r="80" fill="#FFCC29"/><circle cx="240" cy="200" r="50" fill="#DA291C"/><rect x="225" y="175" width="30" height="50" fill="#FFFFFF"/></svg>
          <span>Portugal</span>
          <span class="pill-count">{len(pt_leads)}</span>
        </button>
        <button class="country-pill-btn" id="pill-all" onclick="setCountry('ALL')">
          <span>🌐 Todos</span>
          <span class="pill-count">{len(all_leads)}</span>
        </button>
      </div>
    </header>

    <div class="stats-grid">
      <div class="stat-card">
        <span class="stat-label">Meta Segura</span>
        <span class="stat-value blue" id="meta-count">25 - 30</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Enviadas</span>
        <span class="stat-value green" id="sent-count">0</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Pendentes</span>
        <span class="stat-value cyan" id="pending-count">15</span>
      </div>
    </div>

    <!-- Botão Principal de Disparo Automático em Sequência -->
    <div class="bulk-action-bar">
      <div class="bulk-action-title">
        <span>⚡ Envio Automático em Sequência</span>
        <span style="font-size: 0.825rem; color: var(--muted); font-weight: normal;">(Com cadência anti-bloqueio)</span>
      </div>
      <button class="btn-bulk-start" onclick="openAutoModal()">
        <span>🚀 Iniciar Disparo Automático</span>
      </button>
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
        <button class="tab-btn active" onclick="setLimit(15)" id="btn-top15">🎯 Top 15</button>
        <button class="tab-btn" onclick="setLimit(30)" id="btn-top30">🔥 Top 30</button>
        <button class="tab-btn" onclick="setLimit(100)" id="btn-all">📋 Todos (<span id="total-badge">{len(br_leads)}</span>)</button>
      </div>
      <input type="text" class="search-input" id="search-input" placeholder="🔍 Filtrar por nome ou cidade..." oninput="renderLeads()">
    </div>

    <div class="leads-list" id="leads-container"></div>
  </div>

  <!-- Modal de Disparo Automático -->
  <div class="modal-backdrop" id="auto-modal">
    <div class="modal-box">
      <div class="modal-header">
        <div class="modal-title">🚀 Disparo Automático de Mensagens</div>
        <button class="modal-close" onclick="closeAutoModal()">&times;</button>
      </div>

      <div style="font-size: 0.95rem; color: #e2e8f0; line-height: 1.45;">
        O sequenciador enviará automaticamente para os <strong id="modal-leads-count" style="color: #38bdf8;">15</strong> leads da fila atual respeitando o intervalo de segurança configurado.
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.3); padding: 0.75rem 1rem; border-radius: 0.75rem;">
        <span style="font-size: 0.9rem; color: var(--muted); font-weight: 600;">Intervalo Anti-Bloqueio:</span>
        <select id="auto-delay-select" style="background: #1e293b; color: #fff; border: 1px solid var(--card-border); padding: 0.4rem 0.8rem; border-radius: 0.5rem; font-weight: 700;">
          <option value="25">25 segundos</option>
          <option value="30" selected>30 segundos (Recomendado)</option>
          <option value="45">45 segundos</option>
          <option value="60">60 segundos (Ultra Seguro)</option>
        </select>
      </div>

      <div style="text-align: center;">
        <div style="font-size: 0.85rem; color: var(--muted); margin-bottom: 0.25rem;" id="modal-status-text">Status: Pronto para iniciar</div>
        <div class="timer-display" id="modal-timer">00s</div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" id="modal-progress-fill"></div>
        </div>
        <div style="font-size: 0.8rem; color: #94a3b8;" id="modal-progress-text">Progresso: 0 / 15 enviados</div>
      </div>

      <div style="display: flex; gap: 0.75rem; margin-top: 0.5rem;">
        <button id="btn-modal-start" onclick="startAutoQueue()" style="flex: 1; background: var(--whatsapp-green); color: #061e0e; border: none; padding: 0.85rem; border-radius: 0.75rem; font-weight: 800; font-size: 1rem; cursor: pointer;">
          ▶ Iniciar Disparos
        </button>
        <button id="btn-modal-stop" onclick="stopAutoQueue()" disabled style="flex: 1; background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.85rem; border-radius: 0.75rem; font-weight: 800; font-size: 1rem; cursor: pointer;">
          ⏹ Parar
        </button>
      </div>
    </div>
  </div>

  <script>
    const LEADS_DATA = {json.dumps(all_leads, ensure_ascii=False)};

    let currentCountry = 'BR'; // 'BR' | 'PT' | 'ALL'
    let currentLimit = 15;
    let sentLeads = JSON.parse(localStorage.getItem('sent_odonto_leads') || '[]');

    let autoRunning = false;
    let autoIndex = 0;
    let autoQueue = [];
    let autoTimerInterval = null;
    let currentCountdown = 0;

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

    function setCountry(country) {{
      currentCountry = country;
      document.getElementById('pill-br').classList.toggle('active', country === 'BR');
      document.getElementById('pill-pt').classList.toggle('active', country === 'PT');
      document.getElementById('pill-all').classList.toggle('active', country === 'ALL');

      const totalBadge = document.getElementById('total-badge');
      if (country === 'BR') {{
        totalBadge.textContent = '{len(br_leads)}';
      }} else if (country === 'PT') {{
        totalBadge.textContent = '{len(pt_leads)}';
      }} else {{
        totalBadge.textContent = '{len(all_leads)}';
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
          (l.whatsapp && l.whatsapp.includes(query))
        );
      }}
      return list.slice(0, currentLimit);
    }}

    function updateStats() {{
      const visibleLeads = getFilteredLeads();
      const sentCount = visibleLeads.filter(lead => sentLeads.includes(lead.name)).length;
      document.getElementById('sent-count').textContent = sentCount;
      document.getElementById('pending-count').textContent = visibleLeads.length - sentCount;
    }}

    function copyLeadMessage(msg, btn) {{
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
        container.innerHTML = '<div style="text-align: center; color: var(--muted); padding: 3rem;">Nenhum consultório encontrado para esta busca.</div>';
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
        const msg = lead.mensagem_personalizada;
        const waLink = lead.wa_link_com_mensagem || `${{lead.wa_link}}?text=${{encodeURIComponent(msg)}}`;

        card.innerHTML = `
          <div class="lead-info">
            <div class="lead-header">
              <span class="lead-number">#${{String(index + 1).padStart(2, '0')}}</span>
              <span class="lead-name">${{lead.name}}</span>
              <span class="rating-badge">★ ${{lead.rating}} (${{lead.reviews}} avaliações)</span>
            </div>
            <div class="lead-details">
              <div class="detail-item"><strong>${{phoneLabel}}:</strong> <span style="font-family: 'JetBrains Mono', monospace; color: #38bdf8; font-weight: 700;">${{lead.whatsapp}}</span></div>
              <div class="detail-item"><strong>Localização:</strong> ${{lead.bairro ? lead.bairro + ' • ' : ''}}${{lead.city_state}}</div>
              <div class="detail-item"><strong>Categorias:</strong> ${{lead.categories}}</div>
            </div>
            <div class="msg-preview">${{msg}}</div>
          </div>
          <div class="lead-actions">
            <a href="${{waLink}}" target="_blank" class="btn-whatsapp" onclick="if(!sentLeads.includes('${{safeName}}')) toggleSent('${{safeName}}')">
              <span>⚡ Abrir WhatsApp</span>
            </a>
            <button class="btn-copy" onclick="copyLeadMessage('${{msg.replace(/'/g, "\\'")}}', this)">
              📋 Copiar
            </button>
            <button class="btn-mark ${{isSent ? 'active' : ''}}" onclick="toggleSent('${{safeName}}')">
              ${{isSent ? '✓ Enviado' : 'Marcar Enviado'}}
            </button>
          </div>
        `;

        container.appendChild(card);
      }});

      updateStats();
    }}

    /* Funções do Disparo Automático */
    function openAutoModal() {{
      const list = getFilteredLeads();
      autoQueue = list;
      document.getElementById('modal-leads-count').textContent = autoQueue.length;
      document.getElementById('modal-progress-text').textContent = `Progresso: 0 / ${{autoQueue.length}} enviados`;
      document.getElementById('auto-modal').classList.add('open');
    }}

    function closeAutoModal() {{
      if (autoRunning) {{
        if (!confirm('Deseja cancelar o disparo em andamento?')) return;
        stopAutoQueue();
      }}
      document.getElementById('auto-modal').classList.remove('open');
    }}

    function startAutoQueue() {{
      if (autoQueue.length === 0) return;
      autoRunning = true;
      autoIndex = 0;
      document.getElementById('btn-modal-start').disabled = true;
      document.getElementById('btn-modal-stop').disabled = false;
      document.getElementById('btn-modal-start').style.opacity = '0.5';

      sendNextInQueue();
    }}

    function stopAutoQueue() {{
      autoRunning = false;
      if (autoTimerInterval) clearInterval(autoTimerInterval);
      document.getElementById('modal-status-text').textContent = 'Status: Disparos interrompidos.';
      document.getElementById('modal-timer').textContent = '00s';
      document.getElementById('btn-modal-start').disabled = false;
      document.getElementById('btn-modal-stop').disabled = true;
      document.getElementById('btn-modal-start').style.opacity = '1';
    }}

    function sendNextInQueue() {{
      if (!autoRunning) return;

      if (autoIndex >= autoQueue.length) {{
        document.getElementById('modal-status-text').textContent = '🎉 Todos os envios da fila foram concluídos!';
        document.getElementById('modal-timer').textContent = 'OK';
        stopAutoQueue();
        return;
      }}

      const lead = autoQueue[autoIndex];
      const msg = lead.mensagem_personalizada;
      const waLink = lead.wa_link_com_mensagem || `${{lead.wa_link}}?text=${{encodeURIComponent(msg)}}`;

      document.getElementById('modal-status-text').innerHTML = `Enviando (#${{autoIndex + 1}}/${{autoQueue.length}}): <strong>${{lead.name}}</strong>`;
      
      // Abre o WhatsApp para o lead atual
      window.open(waLink, '_blank');

      if (!sentLeads.includes(lead.name)) {{
        toggleSent(lead.name);
      }}

      autoIndex++;
      const percent = Math.round((autoIndex / autoQueue.length) * 100);
      document.getElementById('modal-progress-fill').style.width = `${{percent}}%`;
      document.getElementById('modal-progress-text').textContent = `Progresso: ${{autoIndex}} / ${{autoQueue.length}} enviados (${{percent}}%)`;

      if (autoIndex < autoQueue.length) {{
        const delaySec = parseInt(document.getElementById('auto-delay-select').value, 10);
        currentCountdown = delaySec;
        document.getElementById('modal-timer').textContent = `${{currentCountdown}}s`;

        autoTimerInterval = setInterval(() => {{
          if (!autoRunning) {{
            clearInterval(autoTimerInterval);
            return;
          }}
          currentCountdown--;
          document.getElementById('modal-timer').textContent = `${{currentCountdown}}s`;

          if (currentCountdown <= 0) {{
            clearInterval(autoTimerInterval);
            sendNextInQueue();
          }}
        }}, 1000);
      }} else {{
        setTimeout(() => {{
          document.getElementById('modal-status-text').textContent = '🎉 Todos os envios foram finalizados com sucesso!';
          stopAutoQueue();
        }}, 1500);
      }}
    }}

    // Initial render in Brazil mode with Top 15 active
    setCountry('BR');
  </script>
</body>
</html>
"""

with open("disparador_whatsapp.html", "w", encoding="utf-8") as f:
    f.write(html_template)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Dashboard mobile otimizado com sucesso!")
