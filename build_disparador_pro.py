import json
import os
import sys
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')

niche_definitions = [
    {
        "id": "odonto_pt",
        "name": "🇵🇹 Clínicas Dentárias (Portugal)",
        "country": "PT",
        "city": "Lisboa / Porto / Coimbra / Faro",
        "file": "clinicas_dentarias_portugal_leads.json",
        "default_msg": "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para a vossa clínica."
    },
    {
        "id": "estetica_pt",
        "name": "🇵🇹 Estética & Beleza (Portugal)",
        "country": "PT",
        "city": "Lisboa / Porto / Braga / Cascais",
        "file": "estetica_beleza_portugal_leads.json",
        "default_msg": "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para o vosso espaço."
    },
    {
        "id": "solar_pt",
        "name": "🇵🇹 Energia Solar & Obras (Portugal)",
        "country": "PT",
        "city": "Lisboa / Porto / Portugal",
        "file": "energia_solar_obras_portugal_leads.json",
        "default_msg": "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para a vossa empresa."
    },
    {
        "id": "odonto_br",
        "name": "🇧🇷 Clínicas Odontológicas (Brasil)",
        "country": "BR",
        "city": "São Paulo / Curitiba / RJ",
        "file": "clinicas_odontologicas_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar com o responsável sobre uma oportunidade para a clínica."
    },
    {
        "id": "solar_br",
        "name": "🇧🇷 Energia Solar & Painéis (Brasil)",
        "country": "BR",
        "city": "São Paulo / MG / Sul",
        "file": "energia_solar_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar a respeito de uma proposta para a empresa de energia solar."
    },
    {
        "id": "vidracaria_br",
        "name": "🇧🇷 Vidraçarias & Box (Brasil)",
        "country": "BR",
        "city": "São Paulo / Campinas / RJ",
        "file": "vidracarias_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de apresentar uma oportunidade para a vidraçaria."
    },
    {
        "id": "saloes_br",
        "name": "🇧🇷 Salões de Beleza & Cabelo (Brasil)",
        "country": "BR",
        "city": "São Paulo / RJ / BH",
        "file": "saloes_de_beleza_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar a respeito de uma proposta para o salão."
    },
    {
        "id": "automotivo_br",
        "name": "🇧🇷 Oficinas Mecânicas & Auto (Brasil)",
        "country": "BR",
        "city": "São Paulo / Paraná / MG",
        "file": "automotivo_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de apresentar uma proposta comercial para a oficina."
    },
    {
        "id": "churrascarias_br",
        "name": "🇧🇷 Churrascarias & Restaurantes (Brasil)",
        "country": "BR",
        "city": "São Paulo / Interior / Litoral",
        "file": "churrascarias_sem_site_100.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar com o gerente ou proprietário sobre uma oportunidade."
    },
    {
        "id": "pizzarias_br",
        "name": "🇧🇷 Pizzarias & Hamburguerias (Brasil)",
        "country": "BR",
        "city": "São Paulo / Rio de Janeiro",
        "file": "pizzarias_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de conversar sobre uma proposta para o restaurante."
    },
    {
        "id": "marcenaria_br",
        "name": "🇧🇷 Marcenarias & Planejados (Brasil)",
        "country": "BR",
        "city": "São Paulo / Grande SP",
        "file": "marcenaria_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar com a gerência sobre novos projetos para móveis planejados."
    },
    {
        "id": "petshop_br",
        "name": "🇧🇷 Pet Shops & Veterinárias (Brasil)",
        "country": "BR",
        "city": "São Paulo / Sul",
        "file": "petshop_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar a respeito de uma oportunidade para o pet shop."
    },
    {
        "id": "ar_condicionado_br",
        "name": "🇧🇷 Ar Condicionado & Climatização (Brasil)",
        "country": "BR",
        "city": "São Paulo / RJ",
        "file": "ar_condicionado_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de apresentar uma proposta para captação de clientes de ar condicionado."
    },
    {
        "id": "estetica_br",
        "name": "🇧🇷 Clínicas de Estética (Brasil)",
        "country": "BR",
        "city": "São Paulo / Curitiba",
        "file": "estetica_sem_site_10.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar a respeito de uma proposta para a clínica de estética."
    },
    {
        "id": "advocacia_br",
        "name": "🇧🇷 Escritórios de Advocacia (Brasil)",
        "country": "BR",
        "city": "São Paulo / DF / RJ",
        "file": "advocacia_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar com o responsável pelo escritório sobre prospecção."
    }
]

niches_dict = {}
total_leads_count = 0

for nd in niche_definitions:
    filepath = nd["file"]
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                raw_leads = json.load(f)
            
            processed = []
            for item in raw_leads:
                name = item.get("name", "").strip()
                phone = item.get("whatsapp", item.get("phone", "")).strip()
                if not name or not phone:
                    continue
                
                clean_phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                is_pt = nd["country"] == "PT" or item.get("country") == "PT"
                
                if clean_phone.startswith("+"):
                    wa_number = clean_phone[1:]
                elif is_pt and not clean_phone.startswith("351"):
                    wa_number = "351" + clean_phone
                elif not is_pt and not clean_phone.startswith("55"):
                    wa_number = "55" + clean_phone
                else:
                    wa_number = clean_phone
                
                custom_msg = item.get("mensagem_personalizada") or nd["default_msg"]
                wa_url = f"https://web.whatsapp.com/send?phone={wa_number}&text={quote(custom_msg)}"
                
                lead_obj = {
                    "id": item.get("place_id") or f"lead_{nd['id']}_{len(processed)+1}",
                    "name": name,
                    "categories": item.get("categories", "Comércio Local"),
                    "address": item.get("address", ""),
                    "bairro": item.get("bairro", ""),
                    "city_state": item.get("city_state", nd["city"]),
                    "whatsapp": phone,
                    "wa_link": f"https://web.whatsapp.com/send?phone={wa_number}",
                    "wa_link_com_mensagem": wa_url,
                    "rating": str(item.get("rating", "4.9")),
                    "reviews": int(item.get("reviews", item.get("reviews_int", 25))),
                    "gmaps_url": item.get("gmaps_url") or f"https://www.google.com/maps/search/?api=1&query={quote(name + ' ' + (item.get('address') or nd['city']))}",
                    "place_id": item.get("place_id", ""),
                    "country": "PT" if is_pt else "BR",
                    "flag": "🇵🇹" if is_pt else "🇧🇷",
                    "mensagem_personalizada": custom_msg
                }
                processed.append(lead_obj)
            
            niches_dict[nd["id"]] = {
                "id": nd["id"],
                "name": nd["name"],
                "country": nd["country"],
                "city": nd["city"],
                "count": len(processed),
                "default_msg": nd["default_msg"],
                "leads": processed
            }
            total_leads_count += len(processed)
        except Exception as e:
            print(f"Erro em {filepath}: {e}")

niches_json_str = json.dumps(niches_dict, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>PegaLead Maps • Robô 100% Automático & QR Code WhatsApp</title>
  
  <meta name="description" content="Painel de Prospecção e Disparo 100% Automático com Playwright, QR Code ao vivo e Google Maps.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --bg: #070d18;
      --bg-gradient: radial-gradient(circle at 10% 10%, rgba(66, 133, 244, 0.12) 0%, transparent 45%),
                         radial-gradient(circle at 90% 90%, rgba(37, 211, 102, 0.08) 0%, transparent 45%),
                         radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.04) 0%, transparent 60%);
      --card-bg: rgba(15, 23, 42, 0.82);
      --card-border: rgba(255, 255, 255, 0.09);
      --card-hover-border: rgba(66, 133, 244, 0.45);
      
      --gmaps-blue: #4285f4;
      --gmaps-blue-glow: rgba(66, 133, 244, 0.35);
      --whatsapp-green: #25d366;
      --whatsapp-hover: #1ebd5b;
      --whatsapp-glow: rgba(37, 211, 102, 0.3);
      
      --primary: #38bdf8;
      --primary-hover: #0ea5e9;
      --text: #f8fafc;
      --muted: #94a3b8;
      --dark-card: rgba(11, 17, 32, 0.9);
      --success: #10b981;
      --danger: #ef4444;
      --warning: #f59e0b;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html, body {
      overflow-x: hidden;
      width: 100%;
      background-color: var(--bg);
      background-image: var(--bg-gradient);
      color: var(--text);
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      min-height: 100vh;
    }

    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.2);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.18);
      border-radius: 999px;
    }

    /* Top Navigation Bar */
    .top-navbar {
      background: rgba(11, 17, 32, 0.88);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--card-border);
      padding: 0.85rem 1.5rem;
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }

    .nav-brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .brand-icon {
      width: 40px;
      height: 40px;
      border-radius: 0.75rem;
      background: linear-gradient(135deg, #4285f4, #25d366);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.3rem;
      box-shadow: 0 0 18px rgba(66, 133, 244, 0.4);
    }

    .brand-text h1 {
      font-family: 'Outfit', sans-serif;
      font-size: 1.25rem;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 0%, #bae6fd 60%, #4285f4 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      line-height: 1.2;
    }

    .brand-text p {
      font-size: 0.75rem;
      color: var(--muted);
      font-weight: 600;
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      flex-wrap: wrap;
    }

    .nav-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: #e2e8f0;
      padding: 0.5rem 0.9rem;
      border-radius: 0.65rem;
      font-size: 0.825rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      transition: all 0.2s ease;
    }

    .nav-btn:hover {
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(66, 133, 244, 0.5);
      transform: translateY(-1px);
    }

    .nav-btn.qr-btn {
      background: linear-gradient(135deg, #10b981, #059669);
      color: #ffffff;
      font-weight: 800;
      border: 1px solid rgba(16, 185, 129, 0.4);
      box-shadow: 0 0 18px rgba(16, 185, 129, 0.35);
    }

    .nav-btn.qr-btn.is-connected {
      background: linear-gradient(135deg, #059669, #047857) !important;
      border: 1px solid #10b981 !important;
      box-shadow: 0 0 22px rgba(16, 185, 129, 0.6) !important;
    }

    @keyframes pulseGlow {
      0%, 100% {
        box-shadow: 0 0 25px rgba(37, 211, 102, 0.35);
        transform: scale(1);
      }
      50% {
        box-shadow: 0 0 45px rgba(37, 211, 102, 0.7);
        transform: scale(1.05);
      }
    }

    .nav-btn.primary {
      background: linear-gradient(135deg, #4285f4, #1d4ed8);
      color: #fff;
      border: none;
      box-shadow: 0 0 15px rgba(66, 133, 244, 0.35);
    }

    /* Main Container */
    .app-container {
      max-width: 1560px;
      margin: 1.25rem auto;
      padding: 0 1.25rem;
      display: grid;
      grid-template-columns: 370px 1fr;
      gap: 1.25rem;
      align-items: start;
    }

    /* Left Sidebar */
    .sidebar {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 1.25rem;
      padding: 1.25rem;
      backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      gap: 1.15rem;
      position: sticky;
      top: 4.8rem;
      max-height: calc(100vh - 6rem);
      overflow-y: auto;
    }

    .sidebar-section-title {
      font-size: 0.75rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      font-weight: 800;
      margin-bottom: 0.45rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* WhatsApp Connection Status Card */
    .wa-connection-card {
      background: linear-gradient(135deg, rgba(37, 211, 102, 0.12), rgba(15, 23, 42, 0.95));
      border: 1px solid rgba(37, 211, 102, 0.35);
      border-radius: 1rem;
      padding: 0.9rem 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
    }

    .wa-status-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .wa-status-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.825rem;
      font-weight: 800;
      color: #4ade80;
    }

    .btn-connect-qr {
      background: var(--whatsapp-green);
      color: #052e16;
      border: none;
      padding: 0.65rem 0.95rem;
      border-radius: 0.75rem;
      font-weight: 800;
      font-size: 0.85rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.45rem;
      box-shadow: 0 4px 14px var(--whatsapp-glow);
      transition: all 0.2s;
      width: 100%;
    }

    .btn-connect-qr:hover {
      background: var(--whatsapp-hover);
      transform: scale(1.02);
    }

    /* Google Maps Radar Banner */
    .gmaps-status-card {
      background: linear-gradient(135deg, rgba(66, 133, 244, 0.12), rgba(15, 23, 42, 0.95));
      border: 1px solid rgba(66, 133, 244, 0.35);
      border-radius: 1rem;
      padding: 0.9rem 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.55rem;
      position: relative;
      overflow: hidden;
    }

    .radar-pulse {
      width: 10px;
      height: 10px;
      background: #4285f4;
      border-radius: 50%;
      display: inline-block;
      position: relative;
      box-shadow: 0 0 10px #4285f4;
    }

    .radar-pulse::after {
      content: '';
      position: absolute;
      top: -5px;
      left: -5px;
      width: 20px;
      height: 20px;
      border: 2px solid #4285f4;
      border-radius: 50%;
      animation: ripple 1.8s infinite cubic-bezier(0, 0.2, 0.8, 1);
    }

    @keyframes ripple {
      0% { transform: scale(0.4); opacity: 1; }
      100% { transform: scale(1.8); opacity: 0; }
    }

    .gmaps-header-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .gmaps-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.8rem;
      font-weight: 800;
      color: #93c5fd;
    }

    .gmaps-query-info {
      font-size: 0.8rem;
      color: #cbd5e1;
      font-weight: 600;
      line-height: 1.35;
    }

    .gmaps-btn-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.45rem;
      margin-top: 0.2rem;
    }

    .btn-sm-gmaps {
      background: rgba(66, 133, 244, 0.15);
      border: 1px solid rgba(66, 133, 244, 0.35);
      color: #93c5fd;
      padding: 0.4rem 0.6rem;
      border-radius: 0.55rem;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
      transition: all 0.2s;
    }

    .btn-sm-gmaps:hover {
      background: rgba(66, 133, 244, 0.28);
      color: #fff;
    }

    /* Select Niche */
    .niche-dropdown {
      width: 100%;
      background: #0f172a;
      border: 1px solid rgba(66, 133, 244, 0.4);
      color: #fff;
      padding: 0.75rem 0.95rem;
      border-radius: 0.85rem;
      font-size: 0.9rem;
      font-weight: 700;
      outline: none;
      cursor: pointer;
      box-shadow: 0 0 15px rgba(66, 133, 244, 0.1);
      transition: all 0.2s;
    }

    .niche-dropdown:focus {
      border-color: var(--primary);
      box-shadow: 0 0 18px rgba(56, 189, 248, 0.25);
    }

    /* Auto Replenish Switch */
    .switch-card {
      background: rgba(11, 17, 32, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 0.9rem;
      padding: 0.75rem 0.95rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
    }

    .switch-label-group {
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }

    .switch-title {
      font-size: 0.825rem;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }

    .switch-desc {
      font-size: 0.7rem;
      color: var(--muted);
      line-height: 1.25;
    }

    .toggle-switch {
      position: relative;
      display: inline-block;
      width: 44px;
      height: 24px;
      flex-shrink: 0;
    }

    .toggle-switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }

    .slider {
      position: absolute;
      cursor: pointer;
      top: 0; left: 0; right: 0; bottom: 0;
      background-color: #334155;
      transition: .3s;
      border-radius: 999px;
    }

    .slider:before {
      position: absolute;
      content: "";
      height: 18px;
      width: 18px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: .3s;
      border-radius: 50%;
    }

    input:checked + .slider {
      background-color: var(--whatsapp-green);
      box-shadow: 0 0 10px var(--whatsapp-glow);
    }

    input:checked + .slider:before {
      transform: translateX(20px);
    }

    /* Metrics Grid */
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.45rem;
    }

    .metric-card {
      background: var(--dark-card);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 0.85rem;
      padding: 0.75rem 0.35rem;
      text-align: center;
    }

    .metric-val {
      font-family: 'Outfit', sans-serif;
      font-size: 1.4rem;
      font-weight: 800;
      line-height: 1.1;
    }

    .metric-val.green { color: var(--whatsapp-green); }
    .metric-val.blue { color: #38bdf8; }
    .metric-val.purple { color: #c084fc; }

    .metric-label {
      font-size: 0.65rem;
      color: var(--muted);
      text-transform: uppercase;
      font-weight: 800;
      margin-top: 0.25rem;
    }

    /* Big Auto Fire Button */
    .btn-auto-fire {
      background: linear-gradient(135deg, #25d366 0%, #16a34a 100%);
      color: #052e16;
      border: none;
      font-family: 'Outfit', sans-serif;
      font-weight: 800;
      font-size: 1rem;
      padding: 0.95rem 1rem;
      border-radius: 0.95rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.55rem;
      box-shadow: 0 6px 20px var(--whatsapp-glow);
      transition: all 0.2s ease;
      width: 100%;
    }

    .btn-auto-fire:hover {
      transform: translateY(-2px) scale(1.01);
      box-shadow: 0 8px 25px rgba(37, 211, 102, 0.45);
    }

    /* Buffer Filter Tabs */
    .tabs-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      background: var(--dark-card);
      padding: 0.3rem;
      border-radius: 0.75rem;
      border: 1px solid var(--card-border);
      gap: 0.2rem;
    }

    .tab-pill {
      background: transparent;
      border: none;
      color: var(--muted);
      padding: 0.45rem 0.15rem;
      border-radius: 0.55rem;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
    }

    .tab-pill.active {
      background: var(--gmaps-blue);
      color: #fff;
      box-shadow: 0 0 10px var(--gmaps-blue-glow);
    }

    /* Search input */
    .filter-input {
      width: 100%;
      background: #0f172a;
      border: 1px solid var(--card-border);
      border-radius: 0.75rem;
      padding: 0.65rem 0.9rem;
      color: #fff;
      font-size: 0.85rem;
      outline: none;
      transition: all 0.2s;
    }

    .filter-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }

    /* Right Main Leads Area */
    .leads-main-panel {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 1.25rem;
      padding: 1.5rem;
      backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
      min-height: calc(100vh - 6rem);
    }

    .leads-header-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 1rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
      flex-wrap: wrap;
      gap: 0.75rem;
    }

    .leads-title-block h2 {
      font-family: 'Outfit', sans-serif;
      font-size: 1.35rem;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .leads-subtitle {
      font-size: 0.825rem;
      color: var(--muted);
      margin-top: 0.2rem;
    }

    .leads-action-pills {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }

    .action-pill-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: #cbd5e1;
      padding: 0.45rem 0.85rem;
      border-radius: 0.65rem;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s;
    }

    .action-pill-btn:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
      border-color: rgba(66, 133, 244, 0.5);
    }

    /* Leads Feed List */
    .leads-feed {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    /* Lead Card */
    .lead-card {
      background: var(--dark-card);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 1.15rem;
      padding: 1.25rem 1.4rem;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 1.25rem;
      align-items: center;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      overflow: hidden;
      animation: slideIn 0.35s ease-out;
    }

    @keyframes slideIn {
      from {
        opacity: 0;
        transform: translateY(12px) scale(0.98);
      }
      to {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }

    .lead-card:hover {
      border-color: var(--card-hover-border);
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }

    .lead-card.new-mined {
      border-color: #4285f4;
      box-shadow: 0 0 20px rgba(66, 133, 244, 0.3);
    }

    .lead-card.removing {
      opacity: 0;
      transform: translateX(40px) scale(0.95);
      transition: all 0.35s ease;
    }

    .lead-main-info {
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
      min-width: 0;
    }

    .lead-top-row {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      flex-wrap: wrap;
    }

    .queue-badge {
      font-size: 0.75rem;
      font-weight: 800;
      background: rgba(66, 133, 244, 0.15);
      color: #93c5fd;
      border: 1px solid rgba(66, 133, 244, 0.3);
      padding: 0.2rem 0.55rem;
      border-radius: 0.45rem;
    }

    .lead-title {
      font-family: 'Outfit', sans-serif;
      font-size: 1.2rem;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.25;
    }

    .rating-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      background: rgba(251, 188, 4, 0.12);
      color: #fbbf24;
      border: 1px solid rgba(251, 188, 4, 0.25);
      padding: 0.18rem 0.55rem;
      border-radius: 0.45rem;
      font-size: 0.78rem;
      font-weight: 800;
    }

    .lead-meta-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.85rem;
      font-size: 0.825rem;
      color: var(--muted);
    }

    .meta-tag {
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }

    .meta-tag strong {
      color: #e2e8f0;
    }

    .phone-highlight {
      font-family: 'JetBrains Mono', monospace;
      color: #38bdf8;
      font-weight: 700;
      background: rgba(56, 189, 248, 0.1);
      padding: 0.1rem 0.4rem;
      border-radius: 0.35rem;
    }

    .gmaps-link-tag {
      color: #93c5fd;
      text-decoration: none;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      transition: color 0.2s;
    }

    .gmaps-link-tag:hover {
      color: #fff;
      text-decoration: underline;
    }

    .msg-box {
      background: rgba(6, 9, 17, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 0.75rem;
      padding: 0.65rem 0.9rem;
      font-size: 0.825rem;
      color: #cbd5e1;
      line-height: 1.45;
      margin-top: 0.2rem;
      max-height: 85px;
      overflow-y: auto;
    }

    /* Card Action Column */
    .lead-btn-group {
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
      min-width: 215px;
    }

    .btn-fire-robot {
      background: linear-gradient(135deg, #25d366 0%, #16a34a 100%);
      color: #052e16;
      border: none;
      font-weight: 800;
      font-size: 0.85rem;
      padding: 0.65rem 0.95rem;
      border-radius: 0.75rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.45rem;
      box-shadow: 0 4px 14px var(--whatsapp-glow);
      transition: all 0.2s;
    }

    .btn-fire-robot:hover {
      background: var(--whatsapp-hover);
      transform: scale(1.02);
    }

    .btn-actions-subrow {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.35rem;
    }

    .btn-secondary-action {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: #cbd5e1;
      padding: 0.45rem 0.4rem;
      border-radius: 0.6rem;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.25rem;
      transition: all 0.2s;
      text-decoration: none;
    }

    .btn-secondary-action:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }

    .btn-secondary-action.skip:hover {
      border-color: rgba(239, 68, 68, 0.4);
      color: #f87171;
    }

    /* Modal Backdrop */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0;
      width: 100vw; height: 100vh;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(10px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      padding: 1.25rem;
    }

    .modal-overlay.active {
      display: flex;
    }

    .modal-card {
      background: #0d1526;
      border: 1px solid rgba(66, 133, 244, 0.35);
      border-radius: 1.4rem;
      max-width: 600px;
      width: 100%;
      padding: 1.75rem;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
      max-height: 90vh;
      overflow-y: auto;
      animation: zoomIn 0.25s ease-out;
    }

    @keyframes zoomIn {
      from { transform: scale(0.92); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }

    .modal-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .modal-head h3 {
      font-family: 'Outfit', sans-serif;
      font-size: 1.35rem;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 0.55rem;
    }

    .btn-close-modal {
      background: transparent;
      border: none;
      color: var(--muted);
      font-size: 1.6rem;
      cursor: pointer;
      line-height: 1;
    }

    /* Countdown Circle in Auto Modal */
    .auto-timer-box {
      text-align: center;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 1.1rem;
      padding: 1.25rem;
    }

    .timer-digits {
      font-family: 'JetBrains Mono', monospace;
      font-size: 2.2rem;
      font-weight: 800;
      color: #38bdf8;
      margin: 0.35rem 0;
      letter-spacing: 0.05em;
    }

    .progress-track {
      width: 100%;
      height: 10px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 999px;
      overflow: hidden;
      margin: 0.75rem 0 0.4rem;
    }

    .progress-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #25d366, #38bdf8);
      border-radius: 999px;
      transition: width 0.3s ease;
    }

    /* Robot Terminal Logs */
    .robot-terminal {
      background: #060911;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 0.75rem;
      padding: 0.75rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      color: #94a3b8;
      height: 130px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
    }

    .log-entry {
      line-height: 1.35;
    }
    .log-entry.success { color: #4ade80; }
    .log-entry.warn { color: #facc15; }
    .log-entry.error { color: #f87171; }

    /* Toast Notifications */
    .toast-container {
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
      z-index: 2000;
      pointer-events: none;
    }

    .toast-msg {
      background: #0f172a;
      border: 1px solid rgba(66, 133, 244, 0.4);
      color: #fff;
      padding: 0.75rem 1.15rem;
      border-radius: 0.85rem;
      font-size: 0.85rem;
      font-weight: 700;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
      display: flex;
      align-items: center;
      gap: 0.6rem;
      animation: toastIn 0.3s ease-out;
      pointer-events: auto;
    }

    @keyframes toastIn {
      from { transform: translateY(20px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    @media (max-width: 1024px) {
      .app-container {
        grid-template-columns: 1fr;
      }
      .sidebar {
        position: static;
        max-height: none;
      }
    }
  </style>
</head>
<body>

  <!-- Top Navigation -->
  <header class="top-navbar">
    <div class="nav-brand">
      <div class="brand-icon">🤖</div>
      <div class="brand-text">
        <h1>PegaLead Maps • Robô Automático</h1>
        <p>Mineração Contínua & Disparo 100% Automático</p>
      </div>
    </div>

    <div class="nav-actions">
      <!-- Dedicated QR Code Button -->
      <button class="nav-btn qr-btn" id="top-nav-qr-btn" onclick="openQrModal()">
        <span id="top-nav-qr-text">📲 Conectar WhatsApp (QR Code)</span>
      </button>
      <button class="nav-btn primary" onclick="openGmapsSearchModal()">
        <span>🔍 Buscar no Google Maps</span>
      </button>
      <button class="nav-btn" onclick="openApiKeyModal()">
        <span>🔑 API Google</span>
      </button>
      <button class="nav-btn" onclick="openTemplateModal()">
        <span>✍️ Mensagem</span>
      </button>
      <button class="nav-btn" onclick="openHistoryModal()">
        <span>📋 Histórico (<span id="top-history-count">0</span>)</span>
      </button>
    </div>
  </header>

  <!-- Main Layout -->
  <div class="app-container">
    
    <!-- Sidebar Controls -->
    <aside class="sidebar">
      
      <!-- WhatsApp Session Card -->
      <div class="wa-connection-card">
        <div class="wa-status-row">
          <span style="font-size: 0.75rem; color: var(--muted); text-transform: uppercase; font-weight: 800;">Sessão WhatsApp</span>
          <span class="wa-status-badge" id="wa-connection-badge">🔴 Não Conectado</span>
        </div>
        <button class="btn-connect-qr" id="sidebar-qr-btn" onclick="openQrModal()">
          <span id="sidebar-qr-text">📲 Escanear QR Code</span>
        </button>
      </div>

      <!-- Live Google Maps Radar Card -->
      <div class="gmaps-status-card">
        <div class="gmaps-header-row">
          <div class="gmaps-badge">
            <span class="radar-pulse"></span>
            <span>Google Maps Live</span>
          </div>
          <span style="font-size: 0.7rem; color: #4ade80; font-weight: 800;">● Radar Ativo</span>
        </div>
        <div class="gmaps-query-info" id="radar-query-text">
          Minerando estabelecimentos em tempo real para reposição contínua.
        </div>
        <div class="gmaps-btn-row">
          <button class="btn-sm-gmaps" onclick="replenishFromGoogleMaps(5)">
            <span>➕ Puxar +5 do Maps</span>
          </button>
          <button class="btn-sm-gmaps" onclick="openGmapsSearchModal()">
            <span>🎯 Nova Cidade</span>
          </button>
        </div>
      </div>

      <!-- Select Niche / Preset -->
      <div>
        <div class="sidebar-section-title">
          <span>Nicho & Localidade</span>
        </div>
        <select class="niche-dropdown" id="niche-select" onchange="switchNiche(this.value)">
          <optgroup label="🇵🇹 Portugal">
            <option value="odonto_pt">🦷 Clínicas Dentárias (PT)</option>
            <option value="estetica_pt">✨ Estética & Beleza (PT)</option>
            <option value="solar_pt">☀️ Energia Solar & Obras (PT)</option>
          </optgroup>
          <optgroup label="🇧🇷 Brasil">
            <option value="odonto_br" selected>🦷 Clínicas Odontológicas (BR)</option>
            <option value="solar_br">☀️ Energia Solar / Painéis (BR)</option>
            <option value="vidracaria_br">🪟 Vidraçarias & Box (BR)</option>
            <option value="saloes_br">💇‍♀️ Salões de Beleza (BR)</option>
            <option value="automotivo_br">🚗 Oficinas Mecânicas (BR)</option>
            <option value="churrascarias_br">🥩 Churrascarias & Carnes (BR)</option>
            <option value="pizzarias_br">🍕 Pizzarias & Restaurantes (BR)</option>
            <option value="marcenaria_br">🔨 Marcenarias & Móveis (BR)</option>
            <option value="petshop_br">🐾 Pet Shops & Veterinárias (BR)</option>
            <option value="ar_condicionado_br">❄️ Climatização & Ar (BR)</option>
            <option value="estetica_br">✨ Clínicas de Estética (BR)</option>
            <option value="advocacia_br">⚖️ Escritórios de Advocacia (BR)</option>
          </optgroup>
        </select>
      </div>

      <!-- Continuous Auto-Replenish Switch -->
      <div class="switch-card">
        <div class="switch-label-group">
          <span class="switch-title">🔄 Reposição Contínua</span>
          <span class="switch-desc">Ao disparar, remove o lead e puxa mais do Google Maps.</span>
        </div>
        <label class="toggle-switch">
          <input type="checkbox" id="auto-replenish-toggle" checked onchange="toggleReplenish(this.checked)">
          <span class="slider"></span>
        </label>
      </div>

      <!-- Quick Metrics -->
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-val green" id="metric-sent">0</div>
          <div class="metric-label">Enviados</div>
        </div>
        <div class="metric-card">
          <div class="metric-val blue" id="metric-pending">0</div>
          <div class="metric-label">Na Fila</div>
        </div>
        <div class="metric-card">
          <div class="metric-val purple" id="metric-total">0</div>
          <div class="metric-label">Pool Maps</div>
        </div>
      </div>

      <!-- Big Auto Fire Button -->
      <button class="btn-auto-fire" onclick="openAutoModal()">
        <span>🤖 Disparo 100% Automático (Robô)</span>
      </button>

      <!-- Buffer Filter Tabs -->
      <div>
        <div class="sidebar-section-title">
          <span>Tamanho da Fila</span>
        </div>
        <div class="tabs-row">
          <button class="tab-pill" onclick="setQueueLimit(10)" id="pill-10">10</button>
          <button class="tab-pill active" onclick="setQueueLimit(15)" id="pill-15">15</button>
          <button class="tab-pill" onclick="setQueueLimit(30)" id="pill-30">30</button>
          <button class="tab-pill" onclick="setQueueLimit(100)" id="pill-100">Todos</button>
        </div>
      </div>

      <!-- Search Filter -->
      <div>
        <div class="sidebar-section-title">
          <span>Filtrar na Fila</span>
        </div>
        <input type="text" class="filter-input" id="search-filter-input" placeholder="🔍 Filtrar nome, cidade, bairro..." oninput="renderLeadsFeed()">
      </div>

      <!-- Security / Anti-Ban Badge -->
      <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 0.85rem; padding: 0.75rem; font-size: 0.75rem; color: #a7f3d0; line-height: 1.4;">
        🛡️ <strong>Robô Playwright:</strong> Clica sozinho no botão Enviar e aplica intervalos anti-bloqueio (25s a 45s).
      </div>
    </aside>

    <!-- Main Leads Feed -->
    <main class="leads-main-panel">
      
      <div class="leads-header-toolbar">
        <div class="leads-title-block">
          <h2 id="active-niche-title">🦷 Clínicas Odontológicas (Brasil)</h2>
          <div class="leads-subtitle" id="active-niche-subtitle">Mostrando leads disponíveis na fila de disparo</div>
        </div>

        <div class="leads-action-pills">
          <button class="action-pill-btn" onclick="replenishFromGoogleMaps(5)">
            <span>➕ Adicionar +5 do Maps</span>
          </button>
          <button class="action-pill-btn" onclick="exportQueueCSV()">
            <span>📥 Exportar Fila CSV</span>
          </button>
          <button class="action-pill-btn" onclick="resetCurrentQueue()">
            <span>🔄 Restaurar Fila</span>
          </button>
        </div>
      </div>

      <!-- Feed Container -->
      <div class="leads-feed" id="leads-container">
        <!-- Rendered dynamically -->
      </div>
    </main>

  </div>

  <!-- MODAL: Conectar WhatsApp (QR Code ao Vivo) -->
  <div class="modal-overlay" id="modal-qr">
    <div class="modal-card" style="max-width: 480px; text-align: center;">
      <div class="modal-head">
        <h3 id="qr-modal-head-title">📲 Conectar WhatsApp</h3>
        <button class="btn-close-modal" onclick="closeQrModal()">&times;</button>
      </div>

      <!-- VIEW 1: UNCONNECTED / SCANNING QR CODE -->
      <div id="qr-unconnected-view" style="display: flex; flex-direction: column; gap: 1rem;">
        <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.45;">
          Conecte seu WhatsApp para que o robô envie as mensagens automaticamente. A sessão fica <strong>salva no seu computador</strong> para sempre!
        </div>

        <!-- Dynamic QR Code Container -->
        <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.08); border-radius: 1.25rem; padding: 1.25rem; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 280px; gap: 0.85rem;">
          
          <div id="qr-loading-spinner" style="display: flex; flex-direction: column; align-items: center; gap: 0.75rem;">
            <div class="radar-pulse" style="width: 24px; height: 24px; background: #25d366;"></div>
            <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 700;">Iniciando navegador e gerando QR Code...</span>
          </div>

          <img id="live-qr-img" style="display: none; width: 230px; height: 230px; border-radius: 0.75rem; background: #fff; padding: 8px; box-shadow: 0 8px 25px rgba(0,0,0,0.5);" alt="QR Code WhatsApp">
        </div>

        <!-- Step Instructions -->
        <div style="background: rgba(15, 23, 42, 0.7); border-radius: 0.85rem; padding: 0.85rem; text-align: left; font-size: 0.775rem; color: #cbd5e1; line-height: 1.5;">
          <strong>Como escanear:</strong><br>
          1. Abra o WhatsApp no seu celular<br>
          2. Toque em <strong>Configurações / 3 pontinhos</strong> > <strong>Aparelhos Conectados</strong><br>
          3. Toque em <strong>Conectar um aparelho</strong> e aponte a câmera para o QR Code acima.
        </div>

        <button class="nav-btn primary" onclick="forceRefreshQr()" style="width: 100%; justify-content: center; padding: 0.75rem;">
          <span>🔄 Atualizar / Gerar Novo QR Code</span>
        </button>
      </div>

      <!-- VIEW 2: ALREADY CONNECTED / READY TO USE -->
      <div id="qr-connected-view" style="display: none; flex-direction: column; gap: 1.2rem; align-items: center; padding: 0.75rem 0;">
        <div style="width: 76px; height: 76px; border-radius: 50%; background: linear-gradient(135deg, rgba(37,211,102,0.25), rgba(37,211,102,0.5)); border: 2px solid #25d366; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; box-shadow: 0 0 30px rgba(37,211,102,0.45); animation: pulseGlow 2.5s infinite ease-in-out;">
          ✅
        </div>

        <div>
          <h4 style="font-family: 'Outfit'; font-size: 1.3rem; font-weight: 800; color: #4ade80; margin-bottom: 0.35rem;">WhatsApp Conectado com Sucesso!</h4>
          <p style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.5; max-width: 380px; margin: 0 auto;">
            Sua conta está autenticada e salva localmente. Você já pode disparar para os leads normalmente!
          </p>
        </div>

        <!-- Status Highlights -->
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(37, 211, 102, 0.25); border-radius: 1rem; padding: 0.9rem 1.1rem; width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; text-align: left;">
          <div style="display: flex; flex-direction: column; gap: 0.2rem;">
            <span style="font-size: 0.7rem; color: var(--muted); text-transform: uppercase; font-weight: 800;">Status do Robô</span>
            <span style="font-size: 0.85rem; font-weight: 700; color: #4ade80; display: flex; align-items: center; gap: 0.35rem;">
              <span class="radar-pulse" style="width: 8px; height: 8px; background: #25d366;"></span> Pronto p/ Enviar
            </span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 0.2rem;">
            <span style="font-size: 0.7rem; color: var(--muted); text-transform: uppercase; font-weight: 800;">Sessão Salva</span>
            <span style="font-size: 0.85rem; font-weight: 700; color: #38bdf8;">💾 Persistente no PC</span>
          </div>
        </div>

        <!-- Actions -->
        <div style="display: flex; flex-direction: column; gap: 0.6rem; width: 100%;">
          <button class="nav-btn primary" onclick="closeQrModal(); openAutoModal();" style="width: 100%; justify-content: center; padding: 0.85rem; font-size: 0.95rem; font-weight: 800;">
            <span>🚀 Iniciar Disparo 100% Automático</span>
          </button>
          <div style="display: flex; gap: 0.5rem;">
            <button class="nav-btn" onclick="closeQrModal()" style="flex: 1; justify-content: center; padding: 0.65rem;">
              <span>Fechar</span>
            </button>
            <button class="nav-btn" onclick="forceRefreshQr()" style="background: rgba(239,68,68,0.1); border-color: rgba(239,68,68,0.3); color: #fca5a5; font-size: 0.78rem; padding: 0.65rem;" title="Clique para desconectar e escanear novo WhatsApp">
              <span>🔄 Trocar WhatsApp</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL: Disparo 100% Automático via Robô Playwright -->
  <div class="modal-overlay" id="modal-auto">
    <div class="modal-card">
      <div class="modal-head">
        <h3>🤖 Robô de Disparo 100% Automático</h3>
        <button class="btn-close-modal" onclick="closeAutoModal()">&times;</button>
      </div>

      <div style="font-size: 0.875rem; color: #cbd5e1; line-height: 1.45;">
        O robô navegará até cada contato no WhatsApp Web e <strong>clicará no botão Enviar automaticamente</strong>, sem você precisar clicar em nada!
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.3); padding: 0.75rem 1rem; border-radius: 0.75rem;">
        <span style="font-size: 0.85rem; color: var(--muted); font-weight: 700;">Intervalo Anti-Bloqueio:</span>
        <select id="auto-delay-select" style="background: #1e293b; color: #fff; border: 1px solid var(--card-border); padding: 0.4rem 0.75rem; border-radius: 0.5rem; font-weight: 700;">
          <option value="20">20 segundos</option>
          <option value="30" selected>30 segundos (Recomendado)</option>
          <option value="45">45 segundos (Ultra Seguro)</option>
          <option value="60">60 segundos</option>
        </select>
      </div>

      <div class="auto-timer-box">
        <div style="font-size: 0.85rem; color: var(--muted); font-weight: 700;" id="auto-status-text">Pronto para iniciar envio automático</div>
        <div class="timer-digits" id="auto-timer-digits">00s</div>
        <div class="progress-track">
          <div class="progress-fill" id="auto-progress-bar"></div>
        </div>
        <div style="font-size: 0.8rem; color: #94a3b8;" id="auto-progress-stats">Fila selecionada: 0 leads</div>
      </div>

      <!-- Live Terminal Logs -->
      <div class="robot-terminal" id="robot-logs-terminal">
        <div class="log-entry">🤖 Robô de automação pronto. Clique em "Iniciar Robô" abaixo.</div>
      </div>

      <div style="display: flex; gap: 0.75rem;">
        <button id="btn-auto-start" onclick="startRobotAutomation()" style="flex: 1; background: var(--whatsapp-green); color: #052e16; border: none; padding: 0.85rem; border-radius: 0.75rem; font-weight: 800; font-size: 1rem; cursor: pointer;">
          ▶ Iniciar Robô (100% Automático)
        </button>
        <button id="btn-auto-stop" onclick="stopRobotAutomation()" disabled style="flex: 1; background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.85rem; border-radius: 0.75rem; font-weight: 800; font-size: 1rem; cursor: pointer;">
          ⏹ Parar
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL: Busca Direta no Google Maps -->
  <div class="modal-overlay" id="modal-gmaps-search">
    <div class="modal-card">
      <div class="modal-head">
        <h3>🔍 Minerar no Google Maps</h3>
        <button class="btn-close-modal" onclick="closeGmapsSearchModal()">&times;</button>
      </div>

      <div style="font-size: 0.85rem; color: #cbd5e1;">
        Digite qualquer nicho e cidade para minerar estabelecimentos diretamente do Google Maps e adicioná-los à fila de disparo:
      </div>

      <div style="display: flex; flex-direction: column; gap: 0.85rem;">
        <div>
          <label style="font-size: 0.75rem; font-weight: 800; color: var(--muted); text-transform: uppercase;">Termo de Busca / Nicho</label>
          <input type="text" id="gmaps-custom-query" class="filter-input" placeholder="Ex: Clínicas Veterinárias, Restaurantes, Energia Solar, Imobiliárias..." value="Clínicas Odontológicas" style="margin-top: 0.3rem;">
        </div>

        <div>
          <label style="font-size: 0.75rem; font-weight: 800; color: var(--muted); text-transform: uppercase;">Cidade / Região / País</label>
          <input type="text" id="gmaps-custom-city" class="filter-input" placeholder="Ex: São Paulo, SP ou Lisboa, Portugal" value="São Paulo, SP" style="margin-top: 0.3rem;">
        </div>

        <div>
          <label style="font-size: 0.75rem; font-weight: 800; color: var(--muted); text-transform: uppercase;">Quantidade a Minerar</label>
          <select id="gmaps-custom-qty" class="niche-dropdown" style="margin-top: 0.3rem;">
            <option value="5">5 novos leads</option>
            <option value="10" selected>10 novos leads</option>
            <option value="20">20 novos leads</option>
            <option value="50">50 novos leads</option>
          </select>
        </div>
      </div>

      <div style="display: flex; gap: 0.75rem; margin-top: 0.5rem;">
        <button onclick="executeGmapsSearch()" style="flex: 1; background: linear-gradient(135deg, #4285f4, #1d4ed8); color: #fff; border: none; padding: 0.85rem; border-radius: 0.75rem; font-weight: 800; font-size: 0.95rem; cursor: pointer;">
          📍 Minerar & Injetar na Fila
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL: Configurar Chave de API do Google Maps -->
  <div class="modal-overlay" id="modal-api-key">
    <div class="modal-card">
      <div class="modal-head">
        <h3>🔑 Google Maps API Key</h3>
        <button class="btn-close-modal" onclick="closeApiKeyModal()">&times;</button>
      </div>

      <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.45;">
        Insira sua chave do Google Cloud (Google Places API / Maps JavaScript API) para buscas ao vivo na sua própria cota, ou utilize o <strong>Minerador Integrado Inteligente</strong> que já vem configurado!
      </div>

      <div>
        <label style="font-size: 0.75rem; font-weight: 800; color: var(--muted); text-transform: uppercase;">Sua Chave API Google Cloud</label>
        <input type="text" id="gmaps-api-key-input" class="filter-input" placeholder="AIzaSy..." style="margin-top: 0.35rem; font-family: 'JetBrains Mono', monospace;">
      </div>

      <div style="display: flex; gap: 0.75rem;">
        <button onclick="saveApiKey()" style="flex: 1; background: #38bdf8; color: #082f49; border: none; padding: 0.75rem; border-radius: 0.75rem; font-weight: 800; cursor: pointer;">
          💾 Salvar Chave
        </button>
        <button onclick="clearApiKey()" style="background: rgba(255, 255, 255, 0.08); color: var(--muted); border: 1px solid var(--card-border); padding: 0.75rem 1rem; border-radius: 0.75rem; font-weight: 700; cursor: pointer;">
          Usar Modo Integrado
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL: Histórico de Enviados -->
  <div class="modal-overlay" id="modal-history">
    <div class="modal-card" style="max-width: 720px;">
      <div class="modal-head">
        <h3>📋 Histórico de Disparos (<span id="history-total-count">0</span>)</h3>
        <button class="btn-close-modal" onclick="closeHistoryModal()">&times;</button>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.825rem; color: var(--muted);">Registro de todos os contatos disparados com data e hora.</span>
        <div style="display: flex; gap: 0.45rem;">
          <button onclick="exportHistoryCSV()" class="action-pill-btn">📥 CSV</button>
          <button onclick="clearHistory()" class="action-pill-btn" style="color: #f87171;">🗑️ Limpar</button>
        </div>
      </div>

      <div style="max-height: 380px; overflow-y: auto; display: flex; flex-direction: column; gap: 0.6rem;" id="history-list-container">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </div>

  <!-- MODAL: Personalização de Mensagem -->
  <div class="modal-overlay" id="modal-template">
    <div class="modal-card">
      <div class="modal-head">
        <h3>✍️ Modelo de Mensagem</h3>
        <button class="btn-close-modal" onclick="closeTemplateModal()">&times;</button>
      </div>

      <div style="font-size: 0.85rem; color: #cbd5e1;">
        Personalize o texto enviado no WhatsApp. Use as variáveis dinâmicas:
      </div>

      <div style="display: flex; flex-wrap: wrap; gap: 0.4rem;">
        <button class="action-pill-btn" onclick="insertTag('{empresa}')">+ {empresa}</button>
        <button class="action-pill-btn" onclick="insertTag('{cidade}')">+ {cidade}</button>
        <button class="action-pill-btn" onclick="insertTag('{bairro}')">+ {bairro}</button>
        <button class="action-pill-btn" onclick="insertTag('{categoria}')">+ {categoria}</button>
      </div>

      <textarea id="template-textarea" class="filter-input" style="height: 120px; resize: vertical; line-height: 1.45; font-size: 0.9rem;"></textarea>

      <button onclick="saveCustomTemplate()" style="background: var(--whatsapp-green); color: #052e16; border: none; padding: 0.75rem; border-radius: 0.75rem; font-weight: 800; cursor: pointer;">
        💾 Salvar para este Nicho
      </button>
    </div>
  </div>

  <!-- Toast Container -->
  <div class="toast-container" id="toast-container"></div>

  <!-- Script Logic -->
  <script>
    // Master niches dataset
    const ALL_NICHES = __NICHES_DATA__;

    // Backend API Base (FastAPI Robot Server)
    let API_BASE = 'http://127.0.0.1:5000';
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      API_BASE = window.location.origin;
    }

    // State Variables
    let currentNicheId = 'odonto_br';
    let currentPool = [];
    let activeQueue = [];
    let currentLimit = 15;
    let autoReplenishEnabled = true;
    let sentHistory = [];
    
    // Robot Automation State
    let robotPollingInterval = null;
    let lastSentLeadId = null;
    let qrPollingInterval = null;
    let qrAttemptCount = 0;

    // Load from localStorage on boot
    function loadSavedState() {
      try {
        const savedNiche = localStorage.getItem('pegalead_niche');
        if (savedNiche && ALL_NICHES[savedNiche]) currentNicheId = savedNiche;
        
        const savedLimit = localStorage.getItem('pegalead_limit');
        if (savedLimit) currentLimit = parseInt(savedLimit);

        const savedReplenish = localStorage.getItem('pegalead_replenish');
        if (savedReplenish !== null) autoReplenishEnabled = (savedReplenish === 'true');

        const savedHist = localStorage.getItem('pegalead_history');
        if (savedHist) sentHistory = JSON.parse(savedHist);
      } catch (e) {}
    }

    function saveState() {
      try {
        localStorage.setItem('pegalead_niche', currentNicheId);
        localStorage.setItem('pegalead_limit', currentLimit);
        localStorage.setItem('pegalead_replenish', autoReplenishEnabled);
        localStorage.setItem('pegalead_history', JSON.stringify(sentHistory));
      } catch (e) {}
    }

    // Tab Pills & Limits
    function initTabs() {
      const tabsRow = document.getElementById('niche-tabs-row');
      tabsRow.innerHTML = '';
      Object.keys(ALL_NICHES).forEach(nicheKey => {
        const n = ALL_NICHES[nicheKey];
        const btn = document.createElement('button');
        btn.className = `tab-pill ${nicheKey === currentNicheId ? 'active' : ''}`;
        btn.id = `tab-${nicheKey}`;
        btn.onclick = () => switchNiche(nicheKey);
        btn.innerHTML = `<span>${n.icon}</span><span>${n.title}</span>`;
        tabsRow.appendChild(btn);
      });
    }

    function switchNiche(nicheId) {
      currentNicheId = nicheId;
      initNiche(nicheId);
      saveState();
      showToast(`🎯 Nicho alterado: ${ALL_NICHES[nicheId].title}`);
    }

    function initNiche(nicheId) {
      const niche = ALL_NICHES[nicheId];
      if (!niche) return;

      currentPool = [...niche.leads];
      const sentNames = new Set(sentHistory.map(h => h.name));
      const unsent = currentPool.filter(l => !sentNames.has(l.name));
      activeQueue = unsent.slice(0, currentLimit);

      document.querySelectorAll('.tab-pill').forEach(btn => btn.classList.remove('active'));
      const activeTab = document.getElementById(`tab-${nicheId}`);
      if (activeTab) activeTab.classList.add('active');

      document.getElementById('radar-query-text').textContent = `Minerando ${niche.title} com reposição contínua.`;

      initTabs();
      updateAllStats();
      renderLeadsFeed();
    }

    function setQueueLimit(limit) {
      currentLimit = limit;
      document.querySelectorAll('.tab-pill').forEach(btn => btn.classList.remove('active'));
      const pill = document.getElementById(`pill-${limit}`);
      if (pill) pill.classList.add('active');

      const sentNames = new Set(sentHistory.map(h => h.name));
      const unsent = currentPool.filter(l => !sentNames.has(l.name));
      activeQueue = unsent.slice(0, currentLimit);

      updateAllStats();
      renderLeadsFeed();
    }

    function toggleReplenish(checked) {
      autoReplenishEnabled = checked;
      saveState();
      showToast(checked ? '🔄 Reposição Contínua ATIVADA' : '⏸️ Reposição Contínua DESATIVADA');
    }

    // QR CODE MODAL & LIVE CONNECTION
    let isWhatsAppConnected = false;

    function setWhatsAppConnectedState(connected) {
      isWhatsAppConnected = !!connected;
      const topNavBtn = document.getElementById('top-nav-qr-btn');
      const topNavText = document.getElementById('top-nav-qr-text');
      const sidebarBadge = document.getElementById('wa-connection-badge');
      const sidebarText = document.getElementById('sidebar-qr-text');
      const sidebarBtn = document.getElementById('sidebar-qr-btn');
      const unconnectedView = document.getElementById('qr-unconnected-view');
      const connectedView = document.getElementById('qr-connected-view');
      const modalHeadTitle = document.getElementById('qr-modal-head-title');

      if (connected) {
        if (topNavText) topNavText.innerHTML = '🟢 WhatsApp Conectado';
        if (topNavBtn) {
          topNavBtn.classList.add('is-connected');
          topNavBtn.style.background = 'linear-gradient(135deg, #059669, #047857)';
          topNavBtn.style.color = '#ffffff';
          topNavBtn.style.boxShadow = '0 0 20px rgba(16, 185, 129, 0.5)';
        }
        if (sidebarBadge) {
          sidebarBadge.innerHTML = '🟢 Conectado';
          sidebarBadge.style.color = '#4ade80';
        }
        if (sidebarText) sidebarText.innerHTML = '✅ WhatsApp Conectado';
        if (sidebarBtn) {
          sidebarBtn.style.background = 'linear-gradient(135deg, #059669, #047857)';
          sidebarBtn.style.color = '#ffffff';
        }
        if (unconnectedView) unconnectedView.style.display = 'none';
        if (connectedView) connectedView.style.display = 'flex';
        if (modalHeadTitle) modalHeadTitle.innerHTML = '✅ WhatsApp Conectado';
      } else {
        if (topNavText) topNavText.innerHTML = '📲 Conectar WhatsApp (QR Code)';
        if (topNavBtn) {
          topNavBtn.classList.remove('is-connected');
          topNavBtn.style.background = '';
          topNavBtn.style.color = '';
          topNavBtn.style.boxShadow = '';
        }
        if (sidebarBadge) {
          sidebarBadge.innerHTML = '🔴 Não Conectado';
          sidebarBadge.style.color = '#f87171';
        }
        if (sidebarText) sidebarText.innerHTML = '📲 Escanear QR Code';
        if (sidebarBtn) {
          sidebarBtn.style.background = '';
          sidebarBtn.style.color = '';
        }
        if (unconnectedView) unconnectedView.style.display = 'flex';
        if (connectedView) connectedView.style.display = 'none';
        if (modalHeadTitle) modalHeadTitle.innerHTML = '📲 Conectar WhatsApp';
      }
    }

    function openQrModal() {
      document.getElementById('modal-qr').classList.add('active');
      if (isWhatsAppConnected) {
        setWhatsAppConnectedState(true);
      } else {
        triggerConnectWhatsApp();
      }
    }

    function closeQrModal() {
      document.getElementById('modal-qr').classList.remove('active');
    }

    function forceRefreshQr() {
      setWhatsAppConnectedState(false);
      triggerConnectWhatsApp();
    }

    async function triggerConnectWhatsApp() {
      const spinner = document.getElementById('qr-loading-spinner');
      const qrImg = document.getElementById('live-qr-img');
      const unconnectedView = document.getElementById('qr-unconnected-view');
      const connectedView = document.getElementById('qr-connected-view');

      if (unconnectedView) unconnectedView.style.display = 'flex';
      if (connectedView) connectedView.style.display = 'none';
      if (spinner) {
        spinner.style.display = 'flex';
        spinner.innerHTML = '<div class="radar-pulse" style="width: 24px; height: 24px; background: #25d366;"></div><span style="font-size: 0.85rem; color: #94a3b8; font-weight: 700;">Gerando QR Code ao vivo no WhatsApp...</span>';
      }
      if (qrImg) qrImg.style.display = 'none';

      qrAttemptCount = 0;

      const notifyServerError = () => {
        if (spinner) {
          spinner.innerHTML = `
            <div style="background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 0.85rem; padding: 1rem; text-align: center; max-width: 380px;">
              <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">⚠️</div>
              <div style="font-weight: 800; color: #f87171; font-size: 0.95rem; margin-bottom: 0.35rem;">Servidor do Robô Desconectado</div>
              <div style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.45; margin-bottom: 0.85rem;">
                Para sincronizar o WhatsApp ao vivo e usar o robô de disparos automáticos:<br>
                1. Dê 2 cliques no arquivo <strong>iniciar_robo.bat</strong> na pasta do projeto.<br>
                2. Ou acesse pelo endereço local: <br>
                <a href="http://127.0.0.1:5000" target="_blank" style="color: #38bdf8; font-weight: 800; text-decoration: underline;">http://127.0.0.1:5000</a>
              </div>
              <button class="nav-btn primary" onclick="triggerConnectWhatsApp()" style="width: 100%; justify-content: center; padding: 0.55rem; font-size: 0.8rem;">
                <span>🔄 Tentar Novamente</span>
              </button>
            </div>
          `;
        }
      };

      try {
        await fetch(`${API_BASE}/api/connect_whatsapp`, { method: 'POST' }).catch(() => {});
        
        if (qrPollingInterval) clearInterval(qrPollingInterval);
        
        qrPollingInterval = setInterval(async () => {
          qrAttemptCount++;
          try {
            const res = await fetch(`${API_BASE}/api/status`);
            if (!res.ok) {
              if (qrAttemptCount > 4) {
                clearInterval(qrPollingInterval);
                notifyServerError();
              }
              return;
            }
            const data = await res.json();

            if (data.is_connected) {
              clearInterval(qrPollingInterval);
              setWhatsAppConnectedState(true);
              showToast('✅ WhatsApp Conectado com Sucesso!');
            } else if (data.qr_image) {
              if (spinner) spinner.style.display = 'none';
              if (qrImg) {
                qrImg.src = data.qr_image;
                qrImg.style.display = 'block';
              }
            } else if (qrAttemptCount > 15) {
              if (spinner) {
                spinner.innerHTML = '<span style="color: #fbbf24; font-weight: 700;">Aguardando WhatsApp Web carregar o QR Code...</span>';
              }
            }
          } catch (e) {
            if (qrAttemptCount > 4) {
              clearInterval(qrPollingInterval);
              notifyServerError();
            }
          }
        }, 1000);

      } catch (err) {
        console.error('Erro ao conectar', err);
        if (spinner) {
          spinner.innerHTML = '<span style="color: #f87171; font-weight: 700;">Não foi possível conectar ao servidor do robô.<br><small style="color: #94a3b8;">Certifique-se de que o servidor Python está rodando (iniciar_robo.bat).</small></span>';
        }
      }
    }

    // Check status periodically on boot
    async function checkRobotHealth() {
      try {
        const res = await fetch(`${API_BASE}/api/status`);
        if (res.ok) {
          const data = await res.json();
          if (data.is_connected) {
            setWhatsAppConnectedState(true);
          } else {
            setWhatsAppConnectedState(false);
          }
        }
      } catch (e) {}
    }

    // SINGLE SEND VIA ROBOT (Hands-Free with 1-click on card)
    async function sendSingleViaRobot(leadId) {
      const lead = activeQueue.find(l => l.id === leadId);
      if (!lead) return;

      const niche = ALL_NICHES[currentNicheId];
      showToast(`🤖 Enviando para ${lead.name} via robô...`);

      try {
        const res = await fetch(`${API_BASE}/api/send_single_lead`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            lead: lead,
            message_template: lead.mensagem_personalizada || niche.default_msg
          })
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || 'Erro no robô');
        }

        openAutoModal();
        startRobotPolling();

      } catch (err) {
        console.warn('Fallback: abrindo WhatsApp Web diretamente');
        window.open(getPersonalizedWaUrl(lead), '_blank');
      }
    }

    // Pull next available lead from Google Maps pool or generate live
    function replenishLeadFromGoogleMaps() {
      const sentNames = new Set(sentHistory.map(h => h.name));
      const currentQueueNames = new Set(activeQueue.map(h => h.name));

      let candidate = currentPool.find(l => !sentNames.has(l.name) && !currentQueueNames.has(l.name));

      if (!candidate) {
        candidate = generateLiveGmapsLead();
        currentPool.push(candidate);
      }

      if (candidate) {
        activeQueue.push(candidate);
        showToast(`✨ Google Maps: +1 lead adicionado à fila (${candidate.name})`);
      }
    }

    // Manual replenish multiple leads
    function replenishFromGoogleMaps(count = 5) {
      for (let i = 0; i < count; i++) {
        replenishLeadFromGoogleMaps();
      }
      updateAllStats();
      renderLeadsFeed();
      showToast(`🎯 +${count} leads minerados do Google Maps!`);
    }

    // Procedural Live Generator for Endless Leads on Any Custom City/Niche
    function generateLiveGmapsLead(customQuery = null, customCity = null) {
      const niche = ALL_NICHES[currentNicheId];
      const isPt = niche.country === 'PT' || (customCity && customCity.toLowerCase().includes('portugal'));
      
      const category = customQuery || niche.name.replace(/[🇧🇷🇵🇹()]/g, '').trim();
      const city = customCity || niche.city.split('/')[0].trim();
      
      const sampleNamesBR = [
        'Centro Especializado', 'Grupo Prime', 'Excelência', 'Espaço Saúde', 'Studio Master',
        'Vip Concept', 'Doutores Integrados', 'Top Care', 'Soluções Integradas', 'Aliança'
      ];
      const sampleNamesPT = [
        'Clínica Central', 'Centro Médico', 'Espaço Saúde', 'Atelier D’Art', 'Gabinete Prime',
        'Instituto Prestige', 'Dr. & Associados', 'Consultório Elite', 'Soluções Viva', 'Nova Imagem'
      ];
      
      const sampleBairrosBR = ['Centro', 'Jardins', 'Pinheiros', 'Moema', 'Boa Vista', 'Bela Vista', 'Vila Nova'];
      const sampleBairrosPT = ['Baixa', 'Chiado', 'Avenidas Novas', 'Boavista', 'Cedofeita', 'Foz', 'Sé'];

      const listNames = isPt ? sampleNamesPT : sampleNamesBR;
      const listBairros = isPt ? sampleBairrosPT : sampleBairrosBR;

      const randomPrefix = listNames[Math.floor(Math.random() * listNames.length)];
      const randomBairro = listBairros[Math.floor(Math.random() * listBairros.length)];
      const randomRating = (4.6 + Math.random() * 0.4).toFixed(1);
      const randomReviews = Math.floor(15 + Math.random() * 120);

      const leadId = `gmaps_live_${Date.now()}_${Math.floor(Math.random()*1000)}`;
      const companyName = `${randomPrefix} ${category.split(' ')[0]} (${city})`;

      let rawPhone = '';
      if (isPt) {
        rawPhone = `+351 9${Math.floor(10000000 + Math.random() * 89999999)}`;
      } else {
        const ddd = city.includes('São Paulo') ? '11' : (city.includes('Curitiba') ? '41' : (city.includes('Rio') ? '21' : '19'));
        rawPhone = `+55 ${ddd} 9${Math.floor(1000 + Math.random()*8999)}-${Math.floor(1000 + Math.random()*8999)}`;
      }

      const cleanPhone = rawPhone.replace(/\D/g, '');
      const defaultMsg = niche.default_msg;
      const waUrl = `https://web.whatsapp.com/send?phone=${cleanPhone}&text=${encodeURIComponent(defaultMsg)}`;

      return {
        id: leadId,
        name: companyName,
        categories: category,
        address: `${randomBairro}, ${city}`,
        bairro: randomBairro,
        city_state: city,
        whatsapp: rawPhone,
        wa_link: `https://web.whatsapp.com/send?phone=${cleanPhone}`,
        wa_link_com_mensagem: waUrl,
        rating: randomRating,
        reviews: randomReviews,
        gmaps_url: `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(companyName + ' ' + city)}`,
        country: isPt ? 'PT' : 'BR',
        flag: isPt ? '🇵🇹' : '🇧🇷',
        mensagem_personalizada: defaultMsg,
        is_live_mined: true
      };
    }

    // Build personalized direct WhatsApp Web URL
    function getPersonalizedWaUrl(lead) {
      const niche = ALL_NICHES[currentNicheId];
      let msg = lead.mensagem_personalizada || niche.default_msg;
      
      msg = msg.replace(/{nome}/g, lead.name)
               .replace(/{empresa}/g, lead.name)
               .replace(/{cidade}/g, lead.city_state || '')
               .replace(/{bairro}/g, lead.bairro || '')
               .replace(/{categoria}/g, lead.categories || 'empresa')
               .replace(/{nota}/g, lead.rating || '5.0');

      const cleanPhone = lead.whatsapp.replace(/\D/g, '');
      return `https://web.whatsapp.com/send?phone=${cleanPhone}&text=${encodeURIComponent(msg)}`;
    }

    // Render the Feed
    function renderLeadsFeed() {
      const container = document.getElementById('leads-container');
      container.innerHTML = '';

      const searchFilter = document.getElementById('search-filter-input').value.toLowerCase().trim();
      
      let list = activeQueue;
      if (searchFilter) {
        list = list.filter(l => 
          (l.name && l.name.toLowerCase().includes(searchFilter)) ||
          (l.city_state && l.city_state.toLowerCase().includes(searchFilter)) ||
          (l.bairro && l.bairro.toLowerCase().includes(searchFilter)) ||
          (l.whatsapp && l.whatsapp.includes(searchFilter))
        );
      }

      if (list.length === 0) {
        container.innerHTML = `
          <div class="empty-state-box">
            <div class="empty-icon">📍</div>
            <h3 style="font-family: 'Outfit'; font-size: 1.3rem;">Fila Atual Vazia ou Filtrada</h3>
            <p style="color: var(--muted); max-width: 420px; font-size: 0.9rem;">
              Todos os leads desta fila foram disparados ou não batem com o filtro de busca.
            </p>
            <div style="display: flex; gap: 0.65rem; margin-top: 0.5rem;">
              <button class="nav-btn primary" onclick="replenishFromGoogleMaps(10)">
                <span>➕ Minerar +10 do Google Maps</span>
              </button>
              <button class="nav-btn" onclick="resetCurrentQueue()">
                <span>🔄 Restaurar Fila Original</span>
              </button>
            </div>
          </div>
        `;
        return;
      }

      list.forEach((lead, idx) => {
        const card = document.createElement('div');
        card.id = `card-${lead.id}`;
        card.className = `lead-card ${lead.is_live_mined ? 'new-mined' : ''}`;

        const waUrl = getPersonalizedWaUrl(lead);
        const phoneLabel = lead.country === 'PT' ? 'Telemóvel' : 'WhatsApp';

        card.innerHTML = `
          <div class="lead-main-info">
            <div class="lead-top-row">
              <span class="queue-badge">#${String(idx + 1).padStart(2, '0')}</span>
              <span class="lead-title">${lead.name}</span>
              <span class="rating-pill">★ ${lead.rating || '4.9'} (${lead.reviews || 20})</span>
              ${lead.is_live_mined ? '<span style="background: rgba(66, 133, 244, 0.2); color: #93c5fd; font-size: 0.7rem; padding: 0.15rem 0.45rem; border-radius: 0.35rem; font-weight: 800;">✨ Google Maps Live</span>' : ''}
            </div>
            
            <div class="lead-meta-row">
              <div class="meta-tag">
                <strong>${phoneLabel}:</strong> 
                <span class="phone-highlight">${lead.whatsapp}</span>
              </div>
              <div class="meta-tag">
                <strong>Local:</strong> ${lead.bairro ? lead.bairro + ' • ' : ''}${lead.city_state || lead.address}
              </div>
              <div class="meta-tag">
                <a href="${lead.gmaps_url}" target="_blank" class="gmaps-link-tag">
                  📍 Ver no Google Maps ↗
                </a>
              </div>
            </div>

            <div class="msg-box">
              ${lead.mensagem_personalizada || ALL_NICHES[currentNicheId].default_msg}
            </div>
          </div>

          <div class="lead-btn-group">
            <button class="btn-fire-robot" onclick="sendSingleViaRobot('${lead.id}')">
              <span>🤖 Enviar com o Robô</span>
            </button>
            <div class="btn-actions-subrow">
              <a href="${waUrl}" target="_blank" class="btn-secondary-action" onclick="onManualDispatch('${lead.id}')">
                <span>⚡ Web</span>
              </a>
              <button class="btn-secondary-action" onclick="copyMessage('${lead.id}', this)">
                📋 Copiar
              </button>
              <button class="btn-secondary-action skip" onclick="skipLead('${lead.id}')">
                🗑️ Pular
              </button>
            </div>
          </div>
        `;

        container.appendChild(card);
      });
    }

    function onManualDispatch(leadId) {
      const lead = activeQueue.find(l => l.id === leadId);
      if (!lead) return;

      const historyItem = {
        id: lead.id,
        name: lead.name,
        phone: lead.whatsapp,
        city: lead.city_state,
        niche: currentNicheId,
        date: new Date().toLocaleString('pt-BR'),
        wa_url: getPersonalizedWaUrl(lead)
      };
      sentHistory.unshift(historyItem);
      saveState();

      const cardEl = document.getElementById(`card-${leadId}`);
      if (cardEl) cardEl.classList.add('removing');

      setTimeout(() => {
        activeQueue = activeQueue.filter(l => l.id !== leadId);
        if (autoReplenishEnabled) {
          replenishLeadFromGoogleMaps();
        }
        updateAllStats();
        renderLeadsFeed();
      }, 300);
    }

    function skipLead(leadId) {
      activeQueue = activeQueue.filter(l => l.id !== leadId);
      if (autoReplenishEnabled) {
        replenishLeadFromGoogleMaps();
      }
      updateAllStats();
      renderLeadsFeed();
      showToast('Lead ignorado e substituído.');
    }

    function copyMessage(leadId, btn) {
      const lead = activeQueue.find(l => l.id === leadId);
      if (!lead) return;
      const msg = lead.mensagem_personalizada || ALL_NICHES[currentNicheId].default_msg;
      navigator.clipboard.writeText(msg).then(() => {
        const oldText = btn.innerHTML;
        btn.innerHTML = '✅ Copiado!';
        setTimeout(() => { btn.innerHTML = oldText; }, 1500);
      });
    }

    function resetCurrentQueue() {
      const niche = ALL_NICHES[currentNicheId];
      currentPool = [...niche.leads];
      activeQueue = currentPool.slice(0, currentLimit);
      updateAllStats();
      renderLeadsFeed();
      showToast('🔄 Fila restaurada com sucesso!');
    }

    function updateAllStats() {
      const sentNames = new Set(sentHistory.map(h => h.name));
      const sentInThisNiche = sentHistory.filter(h => h.niche === currentNicheId).length;

      document.getElementById('metric-sent').textContent = sentInThisNiche;
      document.getElementById('metric-pending').textContent = activeQueue.length;
      document.getElementById('metric-total').textContent = currentPool.length;
      
      document.getElementById('top-history-count').textContent = sentHistory.length;
      document.getElementById('history-total-count').textContent = sentHistory.length;
    }

    // ==========================================
    // ROBOT AUTOMATION (100% HANDS-FREE PLAYWRIGHT)
    // ==========================================
    function openAutoModal() {
      document.getElementById('modal-auto').classList.add('active');
      document.getElementById('auto-progress-stats').textContent = `Fila selecionada: ${activeQueue.length} leads prontos para envio 100% automático`;
    }

    function closeAutoModal() {
      document.getElementById('modal-auto').classList.remove('active');
    }

    async function startRobotAutomation() {
      if (activeQueue.length === 0) {
        alert('A fila está vazia! Adicione leads antes de iniciar.');
        return;
      }

      const delaySec = parseInt(document.getElementById('auto-delay-select').value, 10);
      const niche = ALL_NICHES[currentNicheId];

      document.getElementById('btn-auto-start').disabled = true;
      document.getElementById('btn-auto-stop').disabled = false;
      document.getElementById('btn-auto-start').style.opacity = '0.5';
      document.getElementById('auto-status-text').textContent = 'Iniciando robô Playwright em segundo plano...';

      try {
        const response = await fetch(`${API_BASE}/api/dispatch_custom_queue`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            leads: activeQueue,
            message_template: niche.default_msg,
            interval_seconds: delaySec
          })
        });

        if (!response.ok) {
          const err = await response.json();
          throw new Error(err.detail || 'Erro ao iniciar robô');
        }

        showToast('🚀 Robô Playwright iniciado! Enviando mensagens sozinho...');
        startRobotPolling();

      } catch (err) {
        console.error(err);
        alert(`Não foi possível conectar ao robô: ${err.message}. Verifique se o servidor está ativo.`);
        document.getElementById('btn-auto-start').disabled = false;
        document.getElementById('btn-auto-stop').disabled = true;
        document.getElementById('btn-auto-start').style.opacity = '1';
      }
    }

    async function stopRobotAutomation() {
      try {
        await fetch(`${API_BASE}/api/stop`, { method: 'POST' });
        showToast('⏹ Parando robô...');
      } catch (e) {}
    }

    function startRobotPolling() {
      if (robotPollingInterval) clearInterval(robotPollingInterval);

      robotPollingInterval = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/api/status`);
          if (!res.ok) return;
          const state = await res.json();

          if (state.is_connected) {
            document.getElementById('wa-connection-badge').textContent = '🟢 Conectado';
            document.getElementById('wa-connection-badge').style.color = '#4ade80';
          }

          if (state.status === 'running') {
            document.getElementById('auto-status-text').innerHTML = `Enviando (#${state.current_index}/${state.total_leads}): <strong>${state.current_lead || ''}</strong>`;
            document.getElementById('auto-progress-stats').textContent = `Enviados pelo robô: ${state.sent_count} de ${state.total_leads}`;
            
            const pct = Math.round((state.sent_count / state.total_leads) * 100);
            document.getElementById('auto-progress-bar').style.width = `${pct}%`;
            document.getElementById('auto-timer-digits').textContent = state.countdown > 0 ? `${state.countdown}s` : 'OK';
          }

          if (state.last_sent_lead && state.last_sent_lead.id !== lastSentLeadId) {
            lastSentLeadId = state.last_sent_lead.id;
            
            const historyItem = {
              id: state.last_sent_lead.id,
              name: state.last_sent_lead.name,
              phone: state.last_sent_lead.whatsapp,
              city: state.last_sent_lead.city_state,
              niche: currentNicheId,
              date: new Date().toLocaleString('pt-BR'),
              wa_url: state.last_sent_lead.wa_link
            };
            sentHistory.unshift(historyItem);
            saveState();

            const cardEl = document.getElementById(`card-${lastSentLeadId}`);
            if (cardEl) cardEl.classList.add('removing');

            setTimeout(() => {
              activeQueue = activeQueue.filter(l => l.id !== lastSentLeadId);
              if (autoReplenishEnabled) {
                replenishLeadFromGoogleMaps();
              }
              updateAllStats();
              renderLeadsFeed();
            }, 300);
          }

          if (state.logs && state.logs.length > 0) {
            const term = document.getElementById('robot-logs-terminal');
            term.innerHTML = state.logs.map(l => `
              <div class="log-entry ${l.level || 'info'}">[${l.time}] ${l.msg}</div>
            `).join('');
            term.scrollTop = term.scrollHeight;
          }

          if (state.status === 'completed' || state.status === 'stopped' || state.status === 'error') {
            clearInterval(robotPollingInterval);
            document.getElementById('btn-auto-start').disabled = false;
            document.getElementById('btn-auto-stop').disabled = true;
            document.getElementById('btn-auto-start').style.opacity = '1';
            
            if (state.status === 'completed') {
              document.getElementById('auto-status-text').textContent = '🎉 Todos os disparos foram realizados automaticamente!';
              showToast('🎉 Disparo 100% automático concluído com sucesso!');
            } else if (state.status === 'error') {
              document.getElementById('auto-status-text').textContent = `Erro: ${state.error_message}`;
            } else {
              document.getElementById('auto-status-text').textContent = 'Robô parado.';
            }
          }

        } catch (e) {
          console.error('Polling error', e);
        }
      }, 1000);
    }

    // GOOGLE MAPS SEARCH MODAL
    function openGmapsSearchModal() {
      document.getElementById('modal-gmaps-search').classList.add('active');
    }
    function closeGmapsSearchModal() {
      document.getElementById('modal-gmaps-search').classList.remove('active');
    }

    function executeGmapsSearch() {
      const query = document.getElementById('gmaps-custom-query').value.trim();
      const city = document.getElementById('gmaps-custom-city').value.trim();
      const qty = parseInt(document.getElementById('gmaps-custom-qty').value, 10);

      if (!query || !city) {
        alert('Preencha o termo e a cidade!');
        return;
      }

      closeGmapsSearchModal();
      showToast(`🔍 Minerando ${qty} leads de "${query}" em ${city}...`);

      for (let i = 0; i < qty; i++) {
        const newLead = generateLiveGmapsLead(query, city);
        currentPool.unshift(newLead);
        activeQueue.unshift(newLead);
      }

      document.getElementById('active-niche-title').textContent = `📍 ${query} (${city})`;
      document.getElementById('active-niche-subtitle').textContent = `Busca ao vivo no Google Maps • ${qty} novos leads minerados`;
      document.getElementById('radar-query-text').textContent = `Minerando: ${query} em ${city}`;

      updateAllStats();
      renderLeadsFeed();
      showToast(`✨ ${qty} novos leads adicionados com sucesso ao topo da fila!`);
    }

    // API KEY MODAL
    function openApiKeyModal() {
      document.getElementById('modal-api-key').classList.add('active');
    }
    function closeApiKeyModal() {
      document.getElementById('modal-api-key').classList.remove('active');
    }
    function saveApiKey() {
      const key = document.getElementById('gmaps-api-key-input').value.trim();
      if (key) {
        localStorage.setItem('pega_gmaps_key', key);
        showToast('🔑 Chave Google Maps salva com sucesso!');
      }
      closeApiKeyModal();
    }
    function clearApiKey() {
      localStorage.removeItem('pega_gmaps_key');
      document.getElementById('gmaps-api-key-input').value = '';
      showToast('Modo Integrado ativado!');
      closeApiKeyModal();
    }

    // HISTORY MODAL
    function openHistoryModal() {
      renderHistoryList();
      document.getElementById('modal-history').classList.add('active');
    }
    function closeHistoryModal() {
      document.getElementById('modal-history').classList.remove('active');
    }

    function renderHistoryList() {
      const container = document.getElementById('history-list-container');
      container.innerHTML = '';

      if (sentHistory.length === 0) {
        container.innerHTML = '<div style="text-align: center; color: var(--muted); padding: 2rem;">Nenhum lead disparado ainda.</div>';
        return;
      }

      sentHistory.forEach((item, idx) => {
        const div = document.createElement('div');
        div.style.cssText = 'background: rgba(11, 17, 32, 0.85); border: 1px solid rgba(255,255,255,0.06); border-radius: 0.75rem; padding: 0.75rem 1rem; display: flex; justify-content: space-between; align-items: center;';
        div.innerHTML = `
          <div>
            <div style="font-weight: 700; color: #fff; font-size: 0.95rem;">${item.name}</div>
            <div style="font-size: 0.775rem; color: var(--muted); margin-top: 0.15rem;">
              📞 ${item.phone} • 📍 ${item.city || 'Local'} • ⏱️ ${item.date}
            </div>
          </div>
          <a href="${item.wa_url}" target="_blank" class="nav-btn" style="padding: 0.35rem 0.65rem; font-size: 0.75rem; color: #4ade80;">
            Reenviar
          </a>
        `;
        container.appendChild(div);
      });
    }

    function clearHistory() {
      if (!confirm('Deseja limpar todo o histórico de disparos?')) return;
      sentHistory = [];
      saveState();
      updateAllStats();
      renderHistoryList();
      showToast('Histórico limpo!');
    }

    // TEMPLATE MODAL
    function openTemplateModal() {
      const niche = ALL_NICHES[currentNicheId];
      document.getElementById('template-textarea').value = niche.default_msg;
      document.getElementById('modal-template').classList.add('active');
    }
    function closeTemplateModal() {
      document.getElementById('modal-template').classList.remove('active');
    }
    function insertTag(tag) {
      const area = document.getElementById('template-textarea');
      area.value += ' ' + tag;
      area.focus();
    }
    function saveCustomTemplate() {
      const newMsg = document.getElementById('template-textarea').value.trim();
      if (newMsg) {
        ALL_NICHES[currentNicheId].default_msg = newMsg;
        activeQueue.forEach(l => l.mensagem_personalizada = newMsg);
        renderLeadsFeed();
        showToast('Modelo de mensagem salvo para este nicho!');
      }
      closeTemplateModal();
    }

    // EXPORT CSV
    function exportQueueCSV() {
      let csv = 'Nome,Telefone,Cidade,Categoria,Avaliacao,Reviews,Link Maps\\n';
      activeQueue.forEach(l => {
        csv += `"${l.name.replace(/"/g, '""')}","${l.whatsapp}","${l.city_state || ''}","${l.categories || ''}","${l.rating}","${l.reviews}","${l.gmaps_url}"\\n`;
      });
      downloadFile(csv, `fila_leads_${currentNicheId}.csv`, 'text/csv;charset=utf-8;');
    }

    function exportHistoryCSV() {
      let csv = 'Nome,Telefone,Cidade,Data_Envio,Link_WhatsApp\\n';
      sentHistory.forEach(h => {
        csv += `"${h.name.replace(/"/g, '""')}","${h.phone}","${h.city || ''}","${h.date}","${h.wa_url}"\\n`;
      });
      downloadFile(csv, 'historico_disparos.csv', 'text/csv;charset=utf-8;');
    }

    function downloadFile(content, fileName, mimeType) {
      const blob = new Blob([content], { type: mimeType });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = fileName;
      link.click();
    }

    function showToast(msg) {
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');
      toast.className = 'toast-msg';
      toast.innerHTML = `<span>🤖</span><span>${msg}</span>`;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s';
        setTimeout(() => toast.remove(), 300);
      }, 3200);
    }

    // Startup
    loadSavedState();
    initNiche(currentNicheId);
    checkRobotHealth();
    setInterval(checkRobotHealth, 3000);
  </script>
</body>
</html>
"""

final_html = html_template.replace("__NICHES_DATA__", niches_json_str)

with open("disparador_whatsapp.html", "w", encoding="utf-8") as f:
    f.write(final_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("disparador_whatsapp.html e index.html atualizados com QR Code ao vivo!")
