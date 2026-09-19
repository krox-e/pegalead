import json
import os

niche_definitions = [
    {
        "id": "odonto_pt",
        "name": "🇵🇹 Clínicas Dentárias (Portugal)",
        "country": "PT",
        "file": "clinicas_dentarias_portugal_leads.json",
        "default_msg": "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para a vossa clínica."
    },
    {
        "id": "estetica_pt",
        "name": "🇵🇹 Estética & Beleza (Portugal)",
        "country": "PT",
        "file": "estetica_beleza_portugal_leads.json",
        "default_msg": "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para o vosso espaço."
    },
    {
        "id": "solar_pt",
        "name": "🇵🇹 Energia Solar & Obras (Portugal)",
        "country": "PT",
        "file": "energia_solar_obras_portugal_leads.json",
        "default_msg": "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para a vossa empresa."
    },
    {
        "id": "odonto_br",
        "name": "🇧🇷 Clínicas Odontológicas (Brasil)",
        "country": "BR",
        "file": "clinicas_odontologicas_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "solar_br",
        "name": "🇧🇷 Energia Solar & Painéis (Brasil)",
        "country": "BR",
        "file": "energia_solar_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "vidracaria_br",
        "name": "🇧🇷 Vidraçarias & Box (Brasil)",
        "country": "BR",
        "file": "vidracarias_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "saloes_br",
        "name": "🇧🇷 Salões de Beleza & Cabelo (Brasil)",
        "country": "BR",
        "file": "saloes_de_beleza_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "automotivo_br",
        "name": "🇧🇷 Oficinas Mecânicas & Auto (Brasil)",
        "country": "BR",
        "file": "automotivo_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "churrascarias_br",
        "name": "🇧🇷 Churrascarias & Restaurantes (Brasil)",
        "country": "BR",
        "file": "churrascarias_sem_site_100.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "pizzarias_br",
        "name": "🇧🇷 Pizzarias & Hamburguerias (Brasil)",
        "country": "BR",
        "file": "pizzarias_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "marcenaria_br",
        "name": "🇧🇷 Marcenarias & Planejados (Brasil)",
        "country": "BR",
        "file": "marcenaria_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "petshop_br",
        "name": "🇧🇷 Pet Shops & Veterinárias (Brasil)",
        "country": "BR",
        "file": "petshop_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "ar_condicionado_br",
        "name": "🇧🇷 Ar Condicionado & Climatização (Brasil)",
        "country": "BR",
        "file": "ar_condicionado_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "estetica_br",
        "name": "🇧🇷 Clínicas de Estética (Brasil)",
        "country": "BR",
        "file": "estetica_sem_site_10.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    },
    {
        "id": "advocacia_br",
        "name": "🇧🇷 Escritórios de Advocacia (Brasil)",
        "country": "BR",
        "file": "advocacia_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    }
]

niches_data = {}
for n in niche_definitions:
    fpath = n["file"]
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            leads = json.load(f)
            # normalize fields
            for l in leads:
                l["country"] = n["country"]
                if not l.get("mensagem_personalizada"):
                    l["mensagem_personalizada"] = n["default_msg"]
            niches_data[n["id"]] = {
                "id": n["id"],
                "name": n["name"],
                "country": n["country"],
                "leads": leads,
                "count": len(leads)
            }

html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>PegaLead • Painel de Prospecção Internacional</title>
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
        radial-gradient(circle at 10% 10%, rgba(14, 165, 233, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 90%, rgba(37, 211, 102, 0.06) 0%, transparent 40%);
      color: var(--text);
      min-height: 100vh;
      padding: 1.5rem;
    }}

    /* Main App Layout */
    .app-layout {{
      max-width: 1440px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 1.5rem;
      align-items: start;
    }}

    /* Left Sidebar Panel */
    .sidebar-panel {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 1.25rem;
      padding: 1.5rem;
      backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
      position: sticky;
      top: 1.5rem;
      max-height: calc(100vh - 3rem);
      overflow-y: auto;
    }}

    .badge-user {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(14, 165, 233, 0.12);
      border: 1px solid rgba(14, 165, 233, 0.3);
      color: #38bdf8;
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.825rem;
      font-weight: 700;
      align-self: flex-start;
    }}

    .app-brand h1 {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.6rem;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 0%, #bae6fd 50%, #7dd3fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-top: 0.35rem;
      line-height: 1.2;
    }}

    .app-brand p {{
      color: var(--muted);
      font-size: 0.85rem;
      margin-top: 0.25rem;
      line-height: 1.4;
    }}

    /* Niche Selection Group */
    .section-title {{
      font-size: 0.78rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 700;
      margin-bottom: 0.4rem;
    }}

    .niche-select {{
      width: 100%;
      background: #0f172a;
      border: 1px solid rgba(14, 165, 233, 0.4);
      color: #fff;
      padding: 0.75rem 1rem;
      border-radius: 0.85rem;
      font-size: 0.95rem;
      font-weight: 700;
      outline: none;
      cursor: pointer;
      box-shadow: 0 0 15px rgba(14, 165, 233, 0.1);
      transition: all 0.2s;
    }}

    .niche-select:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 15px var(--primary-glow);
    }}

    /* Compact 3-Box Stats */
    .stats-row {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.5rem;
    }}

    .stat-tile {{
      background: rgba(11, 17, 32, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 0.85rem;
      padding: 0.75rem 0.4rem;
      text-align: center;
    }}

    .stat-tile .num {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.3rem;
      font-weight: 800;
    }}

    .stat-tile .lbl {{
      font-size: 0.65rem;
      color: var(--muted);
      text-transform: uppercase;
      font-weight: 700;
      margin-top: 0.15rem;
    }}

    .num.blue {{ color: #38bdf8; }}
    .num.green {{ color: var(--whatsapp-green); }}
    .num.cyan {{ color: #22d3ee; }}

    /* Bulk Button */
    .btn-bulk {{
      background: var(--whatsapp-green);
      color: #061e0e;
      border: none;
      font-weight: 800;
      font-size: 0.95rem;
      padding: 0.85rem 1rem;
      border-radius: 0.85rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      box-shadow: 0 4px 18px var(--whatsapp-glow);
      transition: all 0.2s ease;
      width: 100%;
    }}

    .btn-bulk:hover {{
      background: var(--whatsapp-hover);
      transform: scale(1.02);
    }}

    /* Tabs & Search */
    .tabs {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      background: rgba(11, 17, 32, 0.9);
      padding: 0.35rem;
      border-radius: 0.75rem;
      border: 1px solid var(--card-border);
      gap: 0.25rem;
    }}

    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--muted);
      padding: 0.5rem 0.25rem;
      border-radius: 0.55rem;
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s ease;
      white-space: nowrap;
    }}

    .tab-btn.active {{
      background: var(--primary);
      color: #ffffff;
      box-shadow: 0 0 10px var(--primary-glow);
    }}

    .search-input {{
      width: 100%;
      background: #0f172a;
      border: 1px solid var(--card-border);
      border-radius: 0.75rem;
      padding: 0.65rem 1rem;
      color: #fff;
      font-size: 0.9rem;
      outline: none;
    }}

    .search-input:focus {{
      border-color: var(--primary);
    }}

    .safety-tip {{
      background: rgba(14, 165, 233, 0.06);
      border: 1px solid rgba(14, 165, 233, 0.25);
      border-radius: 0.85rem;
      padding: 0.75rem 0.9rem;
      font-size: 0.78rem;
      color: #cbd5e1;
      line-height: 1.4;
    }}

    /* Right Leads Container with Independent Scroll */
    .leads-panel {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 1.25rem;
      padding: 1.5rem;
      backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
      max-height: calc(100vh - 3rem);
      overflow-y: auto;
      scroll-behavior: smooth;
    }}

    .leads-panel::-webkit-scrollbar {{
      width: 6px;
    }}
    .leads-panel::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.15);
      border-radius: 999px;
    }}

    .leads-panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 0.75rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      flex-wrap: wrap;
      gap: 0.5rem;
    }}

    .leads-count-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.15rem;
      font-weight: 700;
      color: #fff;
    }}

    .leads-list {{
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}

    .lead-card {{
      background: rgba(11, 17, 32, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 1.1rem;
      padding: 1.25rem;
      transition: all 0.2s ease;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 1.25rem;
      align-items: center;
    }}

    .lead-card:hover {{
      border-color: rgba(14, 165, 233, 0.4);
      transform: translateY(-2px);
    }}

    .lead-card.sent {{
      border-color: rgba(16, 185, 129, 0.35);
      background: rgba(16, 185, 129, 0.05);
    }}

    .lead-info {{
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
      min-width: 0;
    }}

    .lead-header {{
      display: flex;
      align-items: center;
      gap: 0.55rem;
      flex-wrap: wrap;
    }}

    .lead-number {{
      font-size: 0.78rem;
      font-weight: 800;
      background: rgba(255, 255, 255, 0.08);
      padding: 0.2rem 0.55rem;
      border-radius: 0.45rem;
      color: var(--muted);
    }}

    .lead-name {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.15rem;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.3;
    }}

    .rating-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      background: rgba(255, 184, 77, 0.12);
      color: #ffb84d;
      padding: 0.2rem 0.55rem;
      border-radius: 0.45rem;
      font-size: 0.8rem;
      font-weight: 700;
    }}

    .lead-details {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.85rem;
      font-size: 0.85rem;
      color: var(--muted);
    }}

    .detail-item {{
      display: flex;
      align-items: center;
      gap: 0.3rem;
    }}

    .detail-item strong {{
      color: #e5e7eb;
    }}

    .msg-preview {{
      background: rgba(6, 9, 17, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 0.65rem;
      padding: 0.75rem 0.95rem;
      font-size: 0.825rem;
      color: #cbd5e1;
      line-height: 1.45;
      margin-top: 0.2rem;
      max-height: 90px;
      overflow-y: auto;
    }}

    .lead-actions {{
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      min-width: 185px;
    }}

    .btn-whatsapp {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.45rem;
      background: var(--whatsapp-green);
      color: #061e0e;
      font-weight: 800;
      font-size: 0.9rem;
      padding: 0.75rem 1.1rem;
      border-radius: 0.75rem;
      text-decoration: none;
      box-shadow: 0 4px 14px var(--whatsapp-glow);
      transition: all 0.2s ease;
      cursor: pointer;
      border: none;
    }}

    .btn-whatsapp:hover {{
      background: var(--whatsapp-hover);
      transform: scale(1.03);
    }}

    .btn-copy {{
      background: rgba(14, 165, 233, 0.12);
      color: #38bdf8;
      border: 1px solid rgba(14, 165, 233, 0.25);
      padding: 0.5rem;
      border-radius: 0.6rem;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
      transition: all 0.2s ease;
    }}

    .btn-copy:hover {{
      background: rgba(14, 165, 233, 0.22);
      color: #fff;
    }}

    .btn-mark {{
      background: rgba(255, 255, 255, 0.05);
      color: var(--muted);
      border: 1px solid var(--card-border);
      padding: 0.5rem;
      border-radius: 0.6rem;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .btn-mark:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
    }}

    .btn-mark.active {{
      background: rgba(16, 185, 129, 0.2);
      color: var(--success);
      border-color: rgba(16, 185, 129, 0.4);
    }}

    /* Modal */
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
      max-width: 520px;
      width: 100%;
      padding: 1.75rem;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
      display: flex;
      flex-direction: column;
      gap: 1.1rem;
    }}

    .progress-bar-bg {{
      width: 100%;
      height: 8px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 999px;
      overflow: hidden;
      margin: 0.4rem 0;
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
      font-size: 1.8rem;
      font-weight: 800;
      color: #38bdf8;
      text-align: center;
    }}

    /* Responsive adjustments for Tablets & Mobile */
    @media (max-width: 991px) {{
      body {{
        padding: 1rem 0.75rem;
      }}

      .app-layout {{
        grid-template-columns: 1fr;
        gap: 1rem;
      }}

      .sidebar-panel {{
        position: static;
        max-height: none;
        padding: 1.15rem;
      }}

      .leads-panel {{
        max-height: none;
        padding: 1.15rem;
      }}

      .lead-card {{
        grid-template-columns: 1fr;
        gap: 0.85rem;
        padding: 1rem;
      }}

      .lead-details {{
        flex-direction: column;
        gap: 0.3rem;
      }}

      .lead-actions {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
        width: 100%;
      }}

      .btn-whatsapp {{
        grid-column: span 2;
      }}
    }}
  </style>
</head>
<body>

  <div class="app-layout">
    <!-- Coluna Esquerda: Painel Fixo de Controle -->
    <aside class="sidebar-panel">
      <div class="badge-user">⚡ Prospecção Ativa • Leonardo</div>
      <div class="app-brand">
        <h1>PegaLead Prospector</h1>
        <p>Mineração & prospecção no <strong>Brasil 🇧🇷</strong> e <strong>Portugal 🇵🇹</strong> no Google Maps.</p>
      </div>

      <!-- Seletor de Nicho -->
      <div>
        <div class="section-title">Nicho / Categoria de Prospecção</div>
        <select class="niche-select" id="niche-select" onchange="changeNiche(this.value)">
          <optgroup label="🇵🇹 Portugal">
            <option value="odonto_pt">🦷 Clínicas Dentárias (26)</option>
            <option value="estetica_pt">✨ Estética & Beleza (50)</option>
            <option value="solar_pt">☀️ Energia Solar & Obras (8)</option>
          </optgroup>
          <optgroup label="🇧🇷 Brasil">
            <option value="odonto_br" selected>🦷 Clínicas Odontológicas (50)</option>
            <option value="solar_br">☀️ Energia Solar / Painéis (37)</option>
            <option value="vidracaria_br">🪟 Vidraçarias & Box (50)</option>
            <option value="saloes_br">💇‍♀️ Salões de Beleza (50)</option>
            <option value="automotivo_br">🚗 Oficinas Automotivas (35)</option>
            <option value="churrascarias_br">🥩 Churrascarias (100)</option>
            <option value="pizzarias_br">🍕 Pizzarias & Lanches (21)</option>
            <option value="marcenaria_br">🔨 Marcenarias & Móveis (31)</option>
            <option value="petshop_br">🐾 Pet Shops & Vet (17)</option>
            <option value="ar_condicionado_br">❄️ Ar Condicionado (11)</option>
            <option value="estetica_br">✨ Clínicas de Estética (10)</option>
            <option value="advocacia_br">⚖️ Advocacia (9)</option>
          </optgroup>
        </select>
      </div>

      <!-- Métricas Compactas -->
      <div class="stats-row">
        <div class="stat-tile">
          <div class="num blue">25-30</div>
          <div class="lbl">Meta Dia</div>
        </div>
        <div class="stat-tile">
          <div class="num green" id="sent-count">0</div>
          <div class="lbl">Enviados</div>
        </div>
        <div class="stat-tile">
          <div class="num cyan" id="pending-count">0</div>
          <div class="lbl">Pendentes</div>
        </div>
      </div>

      <!-- Botão de Disparo Automático -->
      <button class="btn-bulk" onclick="openAutoModal()">
        <span>🚀 Iniciar Disparo Automático</span>
      </button>

      <!-- Filtros de Limite -->
      <div>
        <div class="section-title">Filtro de Quantidade</div>
        <div class="tabs">
          <button class="tab-btn active" onclick="setLimit(15)" id="btn-top15">Top 15</button>
          <button class="tab-btn" onclick="setLimit(30)" id="btn-top30">Top 30</button>
          <button class="tab-btn" onclick="setLimit(100)" id="btn-all">Todos (<span id="total-badge">0</span>)</button>
        </div>
      </div>

      <!-- Busca -->
      <div>
        <div class="section-title">Buscar Lead</div>
        <input type="text" class="search-input" id="search-input" placeholder="🔍 Nome, cidade, bairro..." oninput="renderLeads()">
      </div>

      <!-- Dica de Proteção -->
      <div class="safety-tip">
        🛡️ <strong>Cadência Segura:</strong> 25 a 30 envios diários com intervalo de 30s. Disparo 100% orgânico e seguro.
      </div>
    </aside>

    <!-- Coluna Direita: Área de Leads com Scroll Independente -->
    <main class="leads-panel">
      <div class="leads-panel-header">
        <div class="leads-count-title" id="leads-header-title">Carregando leads...</div>
        <div style="font-size: 0.85rem; color: var(--muted);" id="leads-sub-info"></div>
      </div>

      <div class="leads-list" id="leads-container"></div>
    </main>
  </div>

  <!-- Modal de Disparo Automático -->
  <div class="modal-backdrop" id="auto-modal">
    <div class="modal-box">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 800; color: #fff;">🚀 Disparo Automático</div>
        <button onclick="closeAutoModal()" style="background: transparent; border: none; color: var(--muted); font-size: 1.5rem; cursor: pointer;">&times;</button>
      </div>

      <div style="font-size: 0.9rem; color: #e2e8f0; line-height: 1.45;">
        Disparo sequencial inteligente para os <strong id="modal-leads-count" style="color: #38bdf8;">15</strong> leads da fila atual.
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.3); padding: 0.65rem 0.9rem; border-radius: 0.65rem;">
        <span style="font-size: 0.85rem; color: var(--muted); font-weight: 600;">Intervalo Anti-Bloqueio:</span>
        <select id="auto-delay-select" style="background: #1e293b; color: #fff; border: 1px solid var(--card-border); padding: 0.35rem 0.65rem; border-radius: 0.5rem; font-weight: 700;">
          <option value="25">25 segundos</option>
          <option value="30" selected>30 segundos (Recomendado)</option>
          <option value="45">45 segundos</option>
          <option value="60">60 segundos</option>
        </select>
      </div>

      <div style="text-align: center;">
        <div style="font-size: 0.85rem; color: var(--muted);" id="modal-status-text">Status: Pronto para iniciar</div>
        <div class="timer-display" id="modal-timer">00s</div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" id="modal-progress-fill"></div>
        </div>
        <div style="font-size: 0.78rem; color: #94a3b8;" id="modal-progress-text">Progresso: 0 enviados</div>
      </div>

      <div style="display: flex; gap: 0.65rem;">
        <button id="btn-modal-start" onclick="startAutoQueue()" style="flex: 1; background: var(--whatsapp-green); color: #061e0e; border: none; padding: 0.75rem; border-radius: 0.65rem; font-weight: 800; font-size: 0.95rem; cursor: pointer;">
          ▶ Iniciar
        </button>
        <button id="btn-modal-stop" onclick="stopAutoQueue()" disabled style="flex: 1; background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.75rem; border-radius: 0.65rem; font-weight: 800; font-size: 0.95rem; cursor: pointer;">
          ⏹ Parar
        </button>
      </div>
    </div>
  </div>

  <script>
    const ALL_NICHES = {json.dumps(niches_data, ensure_ascii=False)};

    let currentNicheId = 'odonto_br';
    let currentLimit = 15;
    let sentLeads = JSON.parse(localStorage.getItem('sent_all_leads_v1') || '[]');

    let autoRunning = false;
    let autoIndex = 0;
    let autoQueue = [];
    let autoTimerInterval = null;
    let currentCountdown = 0;

    function saveSentState() {{
      localStorage.setItem('sent_all_leads_v1', JSON.stringify(sentLeads));
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

    function changeNiche(nicheId) {{
      currentNicheId = nicheId;
      document.getElementById('search-input').value = '';
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

    function getCurrentNicheLeads() {{
      const niche = ALL_NICHES[currentNicheId];
      return niche ? niche.leads : [];
    }}

    function getFilteredLeads() {{
      const query = document.getElementById('search-input')?.value.toLowerCase().trim() || '';
      let list = getCurrentNicheLeads();

      if (query) {{
        list = list.filter(l => 
          (l.name && l.name.toLowerCase().includes(query)) || 
          (l.city_state && l.city_state.toLowerCase().includes(query)) ||
          (l.bairro && l.bairro.toLowerCase().includes(query)) ||
          (l.whatsapp && l.whatsapp.includes(query))
        );
      }}
      return list.slice(0, currentLimit);
    }}

    function updateStats() {{
      const allLeadsInNiche = getCurrentNicheLeads();
      const visible = getFilteredLeads();
      const sentCount = visible.filter(lead => sentLeads.includes(lead.name)).length;
      
      document.getElementById('sent-count').textContent = sentCount;
      document.getElementById('pending-count').textContent = visible.length - sentCount;
      document.getElementById('total-badge').textContent = allLeadsInNiche.length;
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

      const niche = ALL_NICHES[currentNicheId];
      const list = getFilteredLeads();

      document.getElementById('leads-header-title').textContent = niche ? niche.name : 'Leads';
      document.getElementById('leads-sub-info').textContent = `Mostrando ${{list.length}} de ${{niche ? niche.count : 0}} disponíveis`;

      if (list.length === 0) {{
        container.innerHTML = '<div style="text-align: center; color: var(--muted); padding: 3rem;">Nenhum lead encontrado para este filtro/nicho.</div>';
        updateStats();
        return;
      }}

      list.forEach((lead, index) => {{
        const isSent = sentLeads.includes(lead.name);
        const card = document.createElement('div');
        card.className = `lead-card ${{isSent ? 'sent' : ''}}`;

        const safeName = lead.name.replace(/'/g, "\\'");
        const isPt = lead.country === 'PT' || currentNicheId.endsWith('_pt');
        const phoneLabel = isPt ? 'Telemóvel' : 'WhatsApp';
        const msg = lead.mensagem_personalizada || (isPt ? "Olá, viva! Gostaria de falar a respeito de uma proposta." : "Olá, tudo bem? Quero falar a respeito de uma proposta.");
        const waLink = lead.wa_link_com_mensagem || `${{lead.wa_link || ('https://wa.me/' + lead.whatsapp.replace(/\\D/g, ''))}}?text=${{encodeURIComponent(msg)}}`;

        card.innerHTML = `
          <div class="lead-info">
            <div class="lead-header">
              <span class="lead-number">#${{String(index + 1).padStart(2, '0')}}</span>
              <span class="lead-name">${{lead.name}}</span>
              <span class="rating-badge">★ ${{lead.rating || '5.0'}} (${{lead.reviews || lead.reviews_int || '0'}})</span>
            </div>
            <div class="lead-details">
              <div class="detail-item"><strong>${{phoneLabel}}:</strong> <span style="font-family: 'JetBrains Mono', monospace; color: #38bdf8; font-weight: 700;">${{lead.whatsapp}}</span></div>
              <div class="detail-item"><strong>Local:</strong> ${{lead.bairro ? lead.bairro + ' • ' : ''}}${{lead.city_state || lead.address || ''}}</div>
              <div class="detail-item"><strong>Categorias:</strong> ${{lead.categories || 'Comércio local'}}</div>
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
        document.getElementById('modal-status-text').textContent = '🎉 Todos os envios foram concluídos!';
        document.getElementById('modal-timer').textContent = 'OK';
        stopAutoQueue();
        return;
      }}

      const lead = autoQueue[autoIndex];
      const isPt = lead.country === 'PT' || currentNicheId.endsWith('_pt');
      const msg = lead.mensagem_personalizada || (isPt ? "Olá, viva! Gostaria de falar a respeito de uma proposta." : "Olá, tudo bem? Quero falar a respeito de uma proposta.");
      const waLink = lead.wa_link_com_mensagem || `${{lead.wa_link || ('https://wa.me/' + lead.whatsapp.replace(/\\D/g, ''))}}?text=${{encodeURIComponent(msg)}}`;

      document.getElementById('modal-status-text').innerHTML = `Enviando (#${{autoIndex + 1}}/${{autoQueue.length}}): <strong>${{lead.name}}</strong>`;
      
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
          document.getElementById('modal-status-text').textContent = '🎉 Todos os envios foram finalizados!';
          stopAutoQueue();
        }}, 1500);
      }}
    }}

    // Render initial niche
    renderLeads();
  </script>
</body>
</html>
"""

with open("disparador_whatsapp.html", "w", encoding="utf-8") as f:
    f.write(html_template)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Painel multi-nicho com layout 2 colunas e scroll lateral gerado com sucesso!")
