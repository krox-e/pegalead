#!/usr/bin/env python3
"""
Servidor Web e Automação de Disparos de WhatsApp Internacional
Desenvolvido para Leonardo automatizar a prospecção de TODOS os nichos no Brasil 🇧🇷 e Portugal 🇵🇹.
"""

import os
import sys
import json
import time
import re
import threading
import random
import base64
from urllib.parse import quote
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import uvicorn

sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI(title="Painel de Automação WhatsApp • Leonardo (Brasil & Portugal)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global automation state
STATE = {
    "status": "idle", # "idle", "starting", "waiting_qr", "running", "paused", "stopped", "completed", "error"
    "qr_image": None, # Base64 PNG
    "current_lead": None,
    "current_index": 0,
    "total_leads": 0,
    "sent_count": 0,
    "fail_count": 0,
    "countdown": 0,
    "error_message": "",
    "logs": [],
    "leads_progress": {} # lead_id: "pending" | "sending" | "sent" | "failed"
}

STATE_LOCK = threading.Lock()
STOP_EVENT = threading.Event()
PAUSE_EVENT = threading.Event()
RUNNER_THREAD: Optional[threading.Thread] = None

USER_DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".whatsapp_session")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,pt-BR;q=0.8,en;q=0.7"
}

VALID_DDDS = {
    11, 12, 13, 14, 15, 16, 17, 18, 19, # SP
    21, 22, 24, # RJ
    27, 28, # ES
    31, 32, 33, 34, 35, 37, 38, # MG
    41, 42, 43, 44, 45, 46, # PR
    47, 48, 49, # SC
    51, 53, 54, 55, # RS
    61, # DF
    62, 64, # GO
    63, # TO
    65, 66, # MT
    67, # MS
    68, 69, # AC, RO
    71, 73, 74, 75, 77, # BA
    79, # SE
    81, 87, # PE
    82, # AL
    83, # PB
    84, # RN
    85, 88, # CE
    86, 89, # PI
    91, 93, 94, # PA
    92, 97, # AM
    95, 96, 98, 99 # RR, AP, MA
}

def is_brazil_phone(cand):
    if not cand or not isinstance(cand, str):
        return False, None, None
    if any(w in cand.lower() for w in ["av.", "avenida", "rua", "r.", "rodovia", "alameda", "travessa", "estrada", "bairro", "cep", "km", "http", "nº"]):
        return False, None, None
        
    digits = re.sub(r'\D', '', cand)
    if digits.startswith("55") and len(digits) == 13:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 12:
        digits = digits[1:]
        
    if len(digits) != 11:
        return False, None, None
        
    ddd = int(digits[:2])
    if ddd not in VALID_DDDS:
        return False, None, None
        
    if digits[2] != '9':
        return False, None, None
    if digits[3] not in '567894':
        return False, None, None
        
    formatted = f"({ddd}) {digits[2:7]}-{digits[7:]}"
    wa_link = f"https://wa.me/55{digits}"
    return True, formatted, wa_link

def is_portugal_phone(cand):
    if not cand or not isinstance(cand, str):
        return False, None, None, False
    if any(w in cand.lower() for w in ["rua", "r.", "av.", "avenida", "alameda", "estrada", "praça", "largo", "bairro", "cep", "http", "nº", "loja", "piso"]):
        return False, None, None, False
    digits = re.sub(r'\D', '', cand)
    if digits.startswith("351") and len(digits) == 12:
        digits = digits[3:]
    elif digits.startswith("00351") and len(digits) == 14:
        digits = digits[5:]
    if len(digits) != 9:
        return False, None, None, False
    is_mobile = digits.startswith("9")
    formatted = f"+351 {digits[0:3]} {digits[3:6]} {digits[6:9]}" if is_mobile else f"+351 {digits[0:2]} {digits[2:5]} {digits[5:9]}"
    wa_link = f"https://wa.me/351{digits}"
    return True, formatted, wa_link, is_mobile

def extract_mobile_phone(item):
    raw_candidates = []
    if len(item) > 178 and item[178] and isinstance(item[178], list) and len(item[178]) > 0:
        p_obj = item[178][0]
        if isinstance(p_obj, list) and len(p_obj) > 0 and isinstance(p_obj[0], str):
            raw_candidates.append(p_obj[0])
        elif isinstance(p_obj, str):
            raw_candidates.append(p_obj)
            
    def search_strings(obj):
        if isinstance(obj, str):
            if any(c.isdigit() for c in obj) and len(obj) < 40:
                raw_candidates.append(obj)
        elif isinstance(obj, list):
            for x in obj:
                search_strings(x)
        elif isinstance(obj, dict):
            for v in obj.values():
                search_strings(v)
    search_strings(item)
    
    # Prioritize Brazil mobile
    for cand in raw_candidates:
        ok, fmt, link = is_brazil_phone(cand)
        if ok:
            return fmt, link, "BR"
            
    # Prioritize Portugal mobile (starts with 9)
    for cand in raw_candidates:
        ok, fmt, link, is_mob = is_portugal_phone(cand)
        if ok and is_mob:
            return fmt, link, "PT"

    # Secondary Portugal fixed line
    for cand in raw_candidates:
        ok, fmt, link, is_mob = is_portugal_phone(cand)
        if ok:
            return fmt, link, "PT"

    return None, None, None

def get_maps_website(item):
    if len(item) > 7 and item[7]:
        if isinstance(item[7], list) and len(item[7]) > 0 and item[7][0]:
            return str(item[7][0]).strip()
        elif isinstance(item[7], str) and item[7].strip():
            return item[7].strip()
    return None

def extract_city_state(address_str, item):
    if len(item) > 2 and item[2] and isinstance(item[2], list) and len(item[2]) > 1:
        part = item[2][1]
        if "-" in part and len(part.strip()) < 40:
            return part.strip()
            
    # Check for Portugal
    if "portugal" in address_str.lower():
        m = re.search(r'\d{4}-\d{3}\s+([A-Za-zÀ-ÿ\s]+)', address_str)
        if m:
            city = m.group(1).split(',')[0].strip()
            return f"{city}, Portugal"
        for c in ["Lisboa", "Porto", "Braga", "Coimbra", "Setúbal", "Faro", "Aveiro", "Leiria", "Guimarães", "Cascais", "Sintra", "Vila Nova de Gaia", "Funchal", "Almada", "Matosinhos", "Viseu", "Évora", "Portimão", "Barreiro", "Amadora", "Maia", "Odivelas"]:
            if c.lower() in address_str.lower():
                return f"{c}, Portugal"
        return "Portugal"

    m = re.search(r'([A-Za-zÀ-ÿ\s]+)\s*-\s*([A-Z]{2})', address_str)
    if m:
        return f"{m.group(1).strip()} - {m.group(2).strip()}"
        
    for c in ["Lisboa", "Porto", "Braga", "Coimbra", "Setúbal", "Faro", "Aveiro", "Leiria", "Guimarães", "Cascais", "Sintra", "Vila Nova de Gaia", "Funchal", "Almada", "Matosinhos"]:
        if c.lower() in address_str.lower():
            return f"{c}, Portugal"

    return "Brasil"

def add_log(msg: str, level: str = "info"):
    timestamp = time.strftime("%H:%M:%S")
    entry = {"time": timestamp, "msg": msg, "level": level}
    with STATE_LOCK:
        STATE["logs"].append(entry)
        if len(STATE["logs"]) > 200:
            STATE["logs"].pop(0)
    print(f"[{timestamp}] {msg}", flush=True)

class StartRequest(BaseModel):
    category: str
    limit: int = 25
    interval_seconds: int = 30
    message_template: str = "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."

class MineRequest(BaseModel):
    query: str
    limit: int = 25
    country: str = "ALL"

def load_leads_by_category(category: str) -> List[Dict[str, Any]]:
    files_map = {
        # Portugal
        "odonto_pt": "clinicas_dentarias_portugal_leads.json",
        "estetica_pt": "estetica_beleza_portugal_leads.json",
        "solar_pt": "energia_solar_obras_portugal_leads.json",
        
        # Brasil
        "solar": "energia_solar_leads.json",
        "vidracaria": "vidracarias_leads.json",
        "saloes": "saloes_de_beleza_leads.json",
        "odonto": "clinicas_odontologicas_leads.json",
        "automotivo": "automotivo_leads.json",
        "pizzarias": "pizzarias_leads.json",
        "marcenaria": "marcenaria_leads.json",
        "petshop": "petshop_leads.json",
        "ar_condicionado": "ar_condicionado_leads.json",
        "churrascarias": "churrascarias_sem_site_100.json",
        "estetica": "estetica_sem_site_10.json",
        "advocacia": "advocacia_leads.json",
        
        # Global / Custom
        "global_odonto": "clinicas_odontologicas_global.json",
        "custom": "custom_leads.json"
    }
    filename = files_map.get(category, "clinicas_odontologicas_global.json")
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure country flag/label
            for item in data:
                if "country" not in item:
                    phone = item.get("whatsapp", "")
                    if phone.startswith("+351") or "Portugal" in item.get("city_state", ""):
                        item["country"] = "PT"
                        item["country_label"] = "Portugal"
                        item["flag"] = "🇵🇹"
                    else:
                        item["country"] = "BR"
                        item["country_label"] = "Brasil"
                        item["flag"] = "🇧🇷"
                else:
                    if item["country"] == "PT":
                        item["country_label"] = "Portugal"
                        item["flag"] = "🇵🇹"
                    else:
                        item["country_label"] = "Brasil"
                        item["flag"] = "🇧🇷"
            return data
    return []

def search_gmaps_live(query: str, limit: int = 25, country: str = "ALL") -> List[Dict[str, Any]]:
    client = httpx.Client(timeout=15.0)
    
    # Enhance query if country specified
    search_q = query
    if country == "PT" and not ("portugal" in query.lower() or any(c in query.lower() for c in ["lisboa", "porto", "braga", "coimbra", "faro", "setubal", "sintra", "cascais"])):
        search_q = f"{query} portugal"
    elif country == "BR" and not ("brasil" in query.lower() or "sp" in query.lower() or "rj" in query.lower()):
        search_q = f"{query} brasil"

    url = f"https://www.google.com/maps/search/{quote(search_q)}"
    try:
        r = client.get(url, headers=HEADERS, follow_redirects=True, timeout=15.0)
        if r.status_code != 200:
            return []
        match = re.search(r'<link href="(/search\?tbm=map[^"]+)"', r.text)
        if not match:
            return []
        sub_url = "https://www.google.com" + match.group(1).replace("&amp;", "&")
        r2 = client.get(sub_url, headers=HEADERS, follow_redirects=True, timeout=15.0)
        if r2.status_code != 200:
            return []
        text = r2.text
        if text.startswith(")]}'"):
            text = text[4:].strip()
        data = json.loads(text)
        if len(data) <= 64 or not data[64]:
            return []
            
        for entry in data[64]:
            if not entry or len(entry) < 2 or not entry[1]:
                continue
            item = entry[1]
            if len(item) < 12 or not item[11]:
                continue
            name = item[11].strip()
            cats = item[13] if len(item) > 13 and isinstance(item[13], list) else []
            
            site = get_maps_website(item)
            if site and not ("business.site" in site or "facebook" in site or "instagram" in site):
                continue
                
            phone_fmt, wa_link, c_code = extract_mobile_phone(item)
            if not phone_fmt:
                continue
                
            address = item[39] if len(item) > 39 and item[39] else (item[18] if len(item) > 18 else "")
            rating = "5.0"
            reviews = 10
            if len(item) > 4 and item[4] and isinstance(item[4], list):
                if len(item[4]) > 7 and item[4][7] is not None:
                    rating = f"{item[4][7]:.1f}"
                elif len(item[4]) > 0 and item[4][0] is not None:
                    rating = f"{item[4][0]:.1f}"
                if len(item[4]) > 8 and item[4][8] is not None:
                    reviews = item[4][8]
            place_id = item[78] if len(item) > 78 and isinstance(item[78], str) else None
            gmaps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}" if place_id else f"https://www.google.com/maps/search/?api=1&query={quote(name + ' ' + address)}"
            city_state = extract_city_state(address, item)
            bairro = item[14] if len(item) > 14 and isinstance(item[14], str) else city_state.split(',')[0]
            
            is_pt = (c_code == "PT") or ("portugal" in address.lower())
            lead_country = "PT" if is_pt else "BR"
            
            # Use authentic PT-PT message for Portugal and PT-BR for Brazil
            short_msg = "Olá, tudo bem? O meu nome é Leonardo, gostaria de falar consigo a respeito de uma proposta." if is_pt else "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
            
            places.append({
                "country": lead_country,
                "country_label": "Portugal" if lead_country == "PT" else "Brasil",
                "flag": "🇵🇹" if lead_country == "PT" else "🇧🇷",
                "lang": "pt-PT" if lead_country == "PT" else "pt-BR",
                "name": name,
                "categories": ", ".join(cats) if cats else query,
                "address": address,
                "bairro": bairro,
                "city_state": city_state,
                "whatsapp": phone_fmt,
                "wa_link": wa_link,
                "rating": rating,
                "reviews": reviews,
                "gmaps_url": gmaps_url,
                "place_id": place_id,
                "instagram": "Não identificado / Sem site",
                "reviews_int": reviews,
                "mensagem_personalizada": short_msg,
                "wa_link_com_mensagem": f"{wa_link}?text={quote(short_msg)}"
            })
            if len(places) >= limit:
                break
        return places
    except Exception as e:
        return []

def run_playwright_automation(leads: List[Dict[str, Any]], message_template: str, interval: int):
    global STATE
    from playwright.sync_api import sync_playwright

    with STATE_LOCK:
        STATE["status"] = "starting"
        STATE["qr_image"] = None
        STATE["total_leads"] = len(leads)
        STATE["current_index"] = 0
        STATE["sent_count"] = 0
        STATE["fail_count"] = 0
        STATE["error_message"] = ""
        STATE["leads_progress"] = {l["name"]: "pending" for l in leads}

    add_log(f"Iniciando navegador Chrome em modo seguro para {len(leads)} leads...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False,
                channel="chrome",
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-infobars",
                    "--start-maximized"
                ],
                ignore_default_args=["--enable-automation"],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
            
            browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
            page = browser.new_page()

            add_log("Acessando WhatsApp Web...")
            page.goto("https://web.whatsapp.com")

            with STATE_LOCK:
                STATE["status"] = "waiting_qr"
            add_log("⏳ Aguardando QR Code e conexão no WhatsApp Web...")

            # Check for QR code or active session
            login_success = False
            for step in range(90): # 180 seconds total
                if STOP_EVENT.is_set():
                    browser.close()
                    with STATE_LOCK:
                        STATE["status"] = "stopped"
                        STATE["qr_image"] = None
                    add_log("Automação cancelada pelo usuário.")
                    return

                try:
                    if page.locator('div[contenteditable="true"], div[data-tab="3"], #side').first.is_visible():
                        login_success = True
                        break
                except Exception:
                    pass

                try:
                    canvas_el = page.locator('canvas').first
                    if canvas_el.is_visible():
                        qr_bytes = canvas_el.screenshot()
                        b64_qr = base64.b64encode(qr_bytes).decode('utf-8')
                        with STATE_LOCK:
                            STATE["qr_image"] = f"data:image/png;base64,{b64_qr}"
                except Exception:
                    pass

                time.sleep(2)

            if not login_success:
                add_log("Tempo de login no WhatsApp expirou. Tente novamente.", level="error")
                with STATE_LOCK:
                    STATE["status"] = "error"
                    STATE["qr_image"] = None
                    STATE["error_message"] = "Tempo de login excedido"
                browser.close()
                return

            with STATE_LOCK:
                STATE["qr_image"] = None
                STATE["status"] = "running"
            add_log("✔ WhatsApp conectado e autenticado com sucesso! Iniciando disparos...", level="success")

            time.sleep(3)

            for idx, lead in enumerate(leads, 1):
                if STOP_EVENT.is_set():
                    add_log("Envio interrompido pelo usuário.", level="warn")
                    break

                while PAUSE_EVENT.is_set():
                    with STATE_LOCK:
                        STATE["status"] = "paused"
                    time.sleep(1)
                    if STOP_EVENT.is_set():
                        break

                with STATE_LOCK:
                    STATE["status"] = "running"
                    STATE["current_index"] = idx
                    STATE["current_lead"] = lead["name"]
                    STATE["leads_progress"][lead["name"]] = "sending"

                name = lead.get("name", "Contato")
                phone = lead.get("whatsapp", "")
                country_flag = lead.get("flag", "📍")
                
                # Format customized message
                msg = message_template.replace("{nome}", name).replace("{cidade}", lead.get("city_state", ""))

                # Clean phone digits and respect international format (PT vs BR)
                digits = "".join(filter(str.isdigit, phone))
                if digits.startswith("351") or digits.startswith("55"):
                    pass
                elif len(digits) == 9 and digits.startswith("9"):
                    digits = f"351{digits}"
                elif len(digits) in [10, 11]:
                    digits = f"55{digits}"

                add_log(f"[{idx}/{len(leads)}] {country_flag} Preparando envio para: {name} ({phone})...")

                send_url = f"https://web.whatsapp.com/send?phone={digits}&text={quote(msg)}"

                try:
                    page.goto(send_url)
                    btn_selector = 'span[data-icon="send"], button[aria-label="Enviar"], button[aria-label="Send"], button[data-tab="11"]'
                    page.wait_for_selector(btn_selector, timeout=28000)
                    time.sleep(random.uniform(2.0, 3.0))
                    page.click(btn_selector)
                    time.sleep(3.0)
                    
                    with STATE_LOCK:
                        STATE["sent_count"] += 1
                        STATE["leads_progress"][lead["name"]] = "sent"
                    
                    add_log(f"✅ Mensagem enviada com sucesso para {name} ({country_flag})!", level="success")

                except Exception as ex:
                    with STATE_LOCK:
                        STATE["fail_count"] += 1
                        STATE["leads_progress"][lead["name"]] = "failed"
                    add_log(f"⚠️ Não foi possível enviar para {name} (Número sem WhatsApp ou timeout).", level="warn")

                if idx < len(leads) and not STOP_EVENT.is_set():
                    actual_delay = interval + random.randint(-2, 4)
                    if actual_delay < 15:
                        actual_delay = 15
                    
                    add_log(f"⏳ Pausa de segurança anti-bloqueio ({actual_delay}s)...")
                    
                    for rem in range(actual_delay, 0, -1):
                        if STOP_EVENT.is_set():
                            break
                        while PAUSE_EVENT.is_set():
                            time.sleep(1)
                            if STOP_EVENT.is_set():
                                break
                        with STATE_LOCK:
                            STATE["countdown"] = rem
                        time.sleep(1)
                    
                    with STATE_LOCK:
                        STATE["countdown"] = 0

            with STATE_LOCK:
                if STOP_EVENT.is_set():
                    STATE["status"] = "stopped"
                else:
                    STATE["status"] = "completed"

            add_log("🎉 Processo de disparo finalizado!", level="success")
            time.sleep(4)
            browser.close()

    except Exception as e:
        add_log(f"Erro na execução da automação: {str(e)}", level="error")
        with STATE_LOCK:
            STATE["status"] = "error"
            STATE["error_message"] = str(e)

@app.get("/api/leads")
def get_leads(category: str = "global_odonto"):
    leads = load_leads_by_category(category)
    return {"category": category, "total": len(leads), "leads": leads}

@app.post("/api/mine")
def mine_niche(req: MineRequest):
    q = req.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Digite uma busca para minerar.")
    
    country_label = "Portugal 🇵🇹" if req.country == "PT" else ("Brasil 🇧🇷" if req.country == "BR" else "Global 🌐")
    add_log(f"🔎 Minerando leads [{country_label}] para: '{q}'...")
    leads = search_gmaps_live(q, limit=req.limit, country=req.country)
    
    with open(os.path.join(os.path.dirname(__file__), "custom_leads.json"), "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
        
    add_log(f"✔ Mineração concluída: {len(leads)} novos leads encontrados sem site!", level="success")
    return {"status": "ok", "query": q, "country": req.country, "total": len(leads), "leads": leads}

@app.get("/api/status")
def get_status():
    with STATE_LOCK:
        return JSONResponse(STATE)

@app.post("/api/start")
def start_automation(req: StartRequest, background_tasks: BackgroundTasks):
    global RUNNER_THREAD
    with STATE_LOCK:
        if STATE["status"] in ["running", "starting", "waiting_qr"]:
            raise HTTPException(status_code=400, detail="Automação já está em andamento.")

    STOP_EVENT.clear()
    PAUSE_EVENT.clear()

    raw_leads = load_leads_by_category(req.category)
    target_leads = raw_leads[:req.limit]

    if not target_leads:
        raise HTTPException(status_code=400, detail="Nenhum lead encontrado para a categoria selecionada.")

    RUNNER_THREAD = threading.Thread(
        target=run_playwright_automation,
        args=(target_leads, req.message_template, req.interval_seconds),
        daemon=True
    )
    RUNNER_THREAD.start()

    return {"status": "started", "total_targets": len(target_leads)}

@app.post("/api/pause")
def pause_automation():
    if PAUSE_EVENT.is_set():
        PAUSE_EVENT.clear()
        add_log("▶ Automação retomada.")
        return {"status": "resumed"}
    else:
        PAUSE_EVENT.set()
        add_log("⏸ Automação pausada.")
        return {"status": "paused"}

@app.post("/api/stop")
def stop_automation():
    STOP_EVENT.set()
    PAUSE_EVENT.clear()
    add_log("⏹ Solicitada parada da automação.")
    return {"status": "stopping"}

# Embedded HTML Interface
@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Robô de Envio Automático WhatsApp Internacional • Leonardo</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --card: rgba(18, 24, 38, 0.85);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #25d366;
      --primary-hover: #1ebd5b;
      --primary-glow: rgba(37, 211, 102, 0.25);
      --cyan: #06b6d4;
      --pink: #ec4899;
      --amber: #f59e0b;
      --purple: #a855f7;
      --red: #ef4444;
      --text: #f8fafc;
      --muted: #94a3b8;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Inter', sans-serif;
      background: var(--bg);
      background-image: 
        radial-gradient(circle at 10% 10%, rgba(37, 211, 102, 0.07) 0%, transparent 40%),
        radial-gradient(circle at 90% 90%, rgba(6, 182, 212, 0.07) 0%, transparent 40%);
      color: var(--text);
      min-height: 100vh;
      padding: 2rem 1.5rem;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .header-title h1 {
      font-family: 'Outfit', sans-serif;
      font-size: 2.2rem;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .header-title p {
      color: var(--muted);
      font-size: 0.95rem;
      margin-top: 0.2rem;
    }

    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.6rem;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      padding: 0.6rem 1.2rem;
      border-radius: 9999px;
      font-weight: 700;
      font-size: 0.95rem;
    }

    .status-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--muted);
    }

    .status-badge.idle .status-dot { background: var(--muted); }
    .status-badge.waiting_qr .status-dot { background: var(--amber); animation: pulse 1.5s infinite; }
    .status-badge.running .status-dot { background: var(--primary); box-shadow: 0 0 10px var(--primary); animation: pulse 1s infinite; }
    .status-badge.paused .status-dot { background: var(--amber); }
    .status-badge.completed .status-dot { background: var(--primary); }
    .status-badge.error .status-dot { background: var(--red); }

    @keyframes pulse {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(1.2); }
      100% { opacity: 1; transform: scale(1); }
    }

    /* Miner Box */
    .miner-card {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.12) 0%, rgba(6, 182, 212, 0.1) 100%);
      border: 1px solid rgba(168, 85, 247, 0.3);
      border-radius: 1.25rem;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }

    .miner-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.5rem;
    }

    .miner-inputs {
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
    }

    .country-select-mini {
      background: rgba(11, 15, 25, 0.9);
      border: 1px solid var(--card-border);
      border-radius: 0.75rem;
      padding: 0.75rem 1rem;
      color: #fff;
      font-weight: 700;
      font-size: 0.9rem;
      min-width: 150px;
    }

    .chips-row {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      align-items: center;
    }

    .chip-btn {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--card-border);
      color: #cbd5e1;
      padding: 0.25rem 0.65rem;
      border-radius: 0.5rem;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }

    .chip-btn:hover {
      background: rgba(168, 85, 247, 0.25);
      border-color: rgba(168, 85, 247, 0.5);
      color: #fff;
    }

    .btn-mine {
      background: var(--purple);
      color: #fff;
      padding: 0.75rem 1.25rem;
      border-radius: 0.75rem;
      font-weight: 700;
      font-size: 0.95rem;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.2s;
      white-space: nowrap;
    }

    .btn-mine:hover {
      background: #9333ea;
      transform: scale(1.02);
    }

    /* Grid Layout */
    .dashboard-grid {
      display: grid;
      grid-template-columns: 410px 1fr;
      gap: 1.5rem;
    }

    @media (max-width: 950px) {
      .dashboard-grid { grid-template-columns: 1fr; }
    }

    .card {
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 1.25rem;
      padding: 1.5rem;
      backdrop-filter: blur(12px);
    }

    .card h2 {
      font-family: 'Outfit', sans-serif;
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 1.25rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    /* QR Code Modal Box */
    .qr-box-container {
      background: rgba(245, 158, 11, 0.08);
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-radius: 1.1rem;
      padding: 1.25rem;
      margin-bottom: 1.5rem;
      text-align: center;
      display: none;
    }

    .qr-box-container.active {
      display: block;
      animation: fadeIn 0.3s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-5px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .qr-img {
      max-width: 220px;
      border-radius: 0.85rem;
      border: 3px solid #fff;
      margin: 0.75rem auto;
      background: #fff;
      padding: 8px;
    }

    /* Config Form */
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
      margin-bottom: 1.2rem;
    }

    label {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    select, input, textarea {
      background: rgba(11, 15, 25, 0.8);
      border: 1px solid var(--card-border);
      border-radius: 0.75rem;
      padding: 0.75rem 1rem;
      color: #fff;
      font-family: inherit;
      font-size: 0.95rem;
      outline: none;
      transition: all 0.2s;
    }

    select:focus, input:focus, textarea:focus {
      border-color: var(--primary);
      box-shadow: 0 0 10px var(--primary-glow);
    }

    textarea {
      resize: vertical;
      min-height: 90px;
      line-height: 1.4;
    }

    .slider-container {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .slider-val {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--primary);
      min-width: 45px;
    }

    /* Action Buttons */
    .btn-group {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      margin-top: 1.5rem;
    }

    button {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 1rem;
      padding: 0.9rem 1.5rem;
      border-radius: 0.85rem;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      transition: all 0.2s;
    }

    .btn-start {
      background: var(--primary);
      color: #061e0e;
      box-shadow: 0 4px 16px var(--primary-glow);
    }

    .btn-start:hover:not(:disabled) {
      background: var(--primary-hover);
      transform: translateY(-1px);
    }

    .btn-pause {
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .btn-stop {
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }

    button:disabled {
      opacity: 0.4;
      cursor: not-allowed;
      transform: none !important;
    }

    /* Stats Grid */
    .stats-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    @media (max-width: 600px) {
      .stats-row { grid-template-columns: repeat(2, 1fr); }
    }

    .stat-box {
      background: rgba(11, 15, 25, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 1rem;
      padding: 1rem;
      text-align: center;
    }

    .stat-box .num {
      font-family: 'Outfit', sans-serif;
      font-size: 1.8rem;
      font-weight: 800;
    }

    .stat-box .lbl {
      font-size: 0.75rem;
      color: var(--muted);
      text-transform: uppercase;
      font-weight: 700;
    }

    /* Progress Bar */
    .progress-wrapper {
      margin-bottom: 1.5rem;
    }

    .progress-bar-bg {
      width: 100%;
      height: 12px;
      background: rgba(255, 255, 255, 0.06);
      border-radius: 999px;
      overflow: hidden;
      margin-top: 0.5rem;
    }

    .progress-bar-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--primary), #38bdf8);
      border-radius: 999px;
      transition: width 0.3s ease;
    }

    /* Logs Terminal */
    .logs-terminal {
      background: #060911;
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 0.85rem;
      padding: 1rem;
      height: 230px;
      overflow-y: auto;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.825rem;
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }

    .log-line {
      display: flex;
      gap: 0.5rem;
      line-height: 1.4;
    }

    .log-time { color: #64748b; }
    .log-info { color: #cbd5e1; }
    .log-success { color: #4ade80; font-weight: 600; }
    .log-warn { color: #fbbf24; }
    .log-error { color: #f87171; font-weight: 600; }

    /* Leads Table */
    .leads-table-container {
      max-height: 250px;
      overflow-y: auto;
      margin-top: 1.5rem;
      border: 1px solid var(--card-border);
      border-radius: 0.85rem;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.875rem;
      text-align: left;
    }

    th {
      background: rgba(11, 15, 25, 0.9);
      padding: 0.75rem 1rem;
      color: var(--muted);
      font-weight: 700;
      position: sticky;
      top: 0;
    }

    td {
      padding: 0.65rem 1rem;
      border-top: 1px solid rgba(255, 255, 255, 0.04);
    }

    .country-tag {
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      padding: 0.15rem 0.5rem;
      border-radius: 0.35rem;
      font-size: 0.75rem;
      font-weight: 700;
    }

    .country-tag.pt { background: rgba(239, 68, 68, 0.15); color: #f87171; }
    .country-tag.br { background: rgba(37, 211, 102, 0.15); color: #4ade80; }

    .tag-status {
      padding: 0.2rem 0.6rem;
      border-radius: 0.4rem;
      font-size: 0.75rem;
      font-weight: 700;
    }

    .tag-pending { background: rgba(255, 255, 255, 0.06); color: var(--muted); }
    .tag-sending { background: rgba(6, 182, 212, 0.15); color: #22d3ee; animation: pulse 1s infinite; }
    .tag-sent { background: rgba(37, 211, 102, 0.15); color: var(--primary); }
    .tag-failed { background: rgba(239, 68, 68, 0.15); color: #f87171; }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div class="header-title">
        <h1>⚡ Disparador Automático WhatsApp • Leonardo</h1>
        <p>Prospecção e envio 100% automático para estabelecimentos no <strong>Brasil 🇧🇷</strong> e <strong>Portugal 🇵🇹</strong>.</p>
      </div>
      <div class="status-badge idle" id="status-badge">
        <div class="status-dot"></div>
        <span id="status-text">Pronto para Iniciar</span>
      </div>
    </header>

    <!-- Minerador Sob Demanda Internacional -->
    <div class="miner-card">
      <div class="miner-top">
        <div>
          <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; color: #fff; margin-bottom: 0.2rem;">🔎 Minerar Qualquer Nicho & Cidade (Brasil 🇧🇷 ou Portugal 🇵🇹)</h3>
          <p style="color: var(--muted); font-size: 0.85rem;">Extraia leads locais sem website com WhatsApp verificado:</p>
        </div>
      </div>

      <div class="chips-row">
        <span style="font-size: 0.75rem; color: var(--muted); font-weight: 700;">Atalhos PT:</span>
        <button class="chip-btn" onclick="fillQuery('clinica dentaria lisboa', 'PT')">🦷 Dentistas Lisboa</button>
        <button class="chip-btn" onclick="fillQuery('clinica estetica porto', 'PT')">✨ Estética Porto</button>
        <button class="chip-btn" onclick="fillQuery('energia solar braga', 'PT')">☀️ Solar Braga</button>
        <button class="chip-btn" onclick="fillQuery('remodelacoes cascais', 'PT')">🔨 Obras Cascais</button>
        <button class="chip-btn" onclick="fillQuery('restaurante coimbra', 'PT')">🍽️ Coimbra</button>
        <button class="chip-btn" onclick="fillQuery('imobiliaria faro', 'PT')">🏠 Faro</button>
      </div>

      <div class="miner-inputs">
        <select id="miner-country" class="country-select-mini">
          <option value="PT">🇵🇹 Portugal</option>
          <option value="BR">🇧🇷 Brasil</option>
          <option value="ALL">🌐 Todos os Países</option>
        </select>
        <input type="text" id="miner-query" placeholder="Ex: clinica dentaria lisboa, oficina mecanica porto..." style="flex: 1;" onkeypress="if(event.key==='Enter') mineCustomNiche()">
        <button class="btn-mine" onclick="mineCustomNiche()" id="btn-mine">
          <span>🔍 Minerar Leads</span>
        </button>
      </div>
    </div>

    <!-- QR Code Box -->
    <div class="qr-box-container" id="qr-box">
      <h3 style="color: #fbbf24; font-family: 'Outfit', sans-serif; font-size: 1.2rem; margin-bottom: 0.35rem;">📱 Escaneie o QR Code com seu WhatsApp</h3>
      <p style="color: #cbd5e1; font-size: 0.9rem;">Abra o WhatsApp no seu celular > <strong>Aparelhos Conectados</strong> > <strong>Conectar um Aparelho</strong> e aponte para a imagem abaixo:</p>
      <div id="qr-image-wrapper">
        <p style="color: var(--muted); padding: 1.5rem;">Carregando QR Code...</p>
      </div>
      <small style="color: var(--muted); font-size: 0.8rem;">Você também pode escanear diretamente na janela do Chrome que foi aberta na sua tela.</small>
    </div>

    <div class="dashboard-grid">
      <!-- Painel de Configuração -->
      <div class="card">
        <h2>⚙️ Configuração do Disparo</h2>

        <div class="form-group">
          <label>Nicho / Lista de Leads</label>
          <select id="category-select" onchange="loadLeadsPreview()">
            <optgroup label="🇵🇹 Portugal">
              <option value="odonto_pt" selected>🦷 Clínicas Dentárias Portugal (26 Leads)</option>
              <option value="estetica_pt">✨ Estética & Beleza Portugal (50 Leads)</option>
              <option value="solar_pt">☀️ Energia Solar & Obras Portugal (8 Leads)</option>
            </optgroup>
            <optgroup label="🇧🇷 Brasil">
              <option value="odonto">🦷 Clínicas Odontológicas Brasil (50 Leads)</option>
              <option value="solar">☀️ Energia Solar / Painéis Brasil (37 Leads)</option>
              <option value="vidracaria">🪟 Vidraçarias / Box e Vidros Brasil (50 Leads)</option>
              <option value="saloes">💇‍♀️ Salões de Beleza Brasil (50 Leads)</option>
              <option value="automotivo">🚗 Oficinas Automotivas Brasil (35 Leads)</option>
              <option value="churrascarias">🥩 Churrascarias Brasil (100 Leads)</option>
              <option value="pizzarias">🍕 Pizzarias & Hamburguerias Brasil (21 Leads)</option>
              <option value="marcenaria">🔨 Marcenarias Brasil (31 Leads)</option>
              <option value="petshop">🐾 Pet Shops Brasil (17 Leads)</option>
              <option value="ar_condicionado">❄️ Ar Condicionado Brasil (11 Leads)</option>
              <option value="estetica">✨ Clínicas de Estética Brasil (10 Leads)</option>
              <option value="advocacia">⚖️ Escritórios de Advocacia Brasil (9 Leads)</option>
            </optgroup>
            <optgroup label="🌐 Internacional & Personalizado">
              <option value="global_odonto">🌎 Odonto Unificado (Brasil + Portugal - 76 Leads)</option>
              <option value="custom">🎯 Leads Minerados Sob Demanda</option>
            </optgroup>
          </select>
        </div>

        <div class="form-group">
          <label>Quantidade de Envios</label>
          <select id="limit-select" onchange="loadLeadsPreview()">
            <option value="10">Top 10 Leads</option>
            <option value="25" selected>Top 25 (Recomendado Diário)</option>
            <option value="50">Top 50 Leads</option>
            <option value="100">Todos os Leads</option>
          </select>
        </div>

        <div class="form-group">
          <label>Intervalo de Segurança Anti-Bloqueio</label>
          <div class="slider-container">
            <input type="range" id="interval-slider" min="15" max="60" value="30" oninput="document.getElementById('slider-val').textContent = this.value + 's'">
            <span class="slider-val" id="slider-val">30s</span>
          </div>
          <small style="color: var(--muted); font-size: 0.75rem; margin-top: 0.2rem;">Intervalo recomendado: 25s a 35s com variação humana.</small>
        </div>

        <div class="form-group">
          <label>Mensagem de Envio</label>
          <textarea id="message-text">Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta.</textarea>
        </div>

        <div class="btn-group">
          <button class="btn-start" id="btn-start" onclick="startAutomation()">
            <span>🚀 Iniciar Envio Automático</span>
          </button>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
            <button class="btn-pause" id="btn-pause" onclick="togglePause()" disabled>
              <span>⏸ Pausar</span>
            </button>
            <button class="btn-stop" id="btn-stop" onclick="stopAutomation()" disabled>
              <span>⏹ Parar</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Painel de Monitoramento & Logs -->
      <div class="card">
        <h2>📊 Monitoramento em Tempo Real</h2>

        <div class="stats-row">
          <div class="stat-box">
            <div class="num" id="stat-total" style="color: #fff;">0</div>
            <div class="lbl">Total da Fila</div>
          </div>
          <div class="stat-box">
            <div class="num" id="stat-sent" style="color: var(--primary);">0</div>
            <div class="lbl">Enviados</div>
          </div>
          <div class="stat-box">
            <div class="num" id="stat-fail" style="color: var(--red);">0</div>
            <div class="lbl">Falhas</div>
          </div>
          <div class="stat-box">
            <div class="num" id="stat-timer" style="color: var(--cyan);">0s</div>
            <div class="lbl">Próximo Envio</div>
          </div>
        </div>

        <div class="progress-wrapper">
          <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
            <span id="current-lead-text" style="font-weight: 600; color: #fff;">Aguardando início...</span>
            <span id="progress-percent" style="font-family: 'JetBrains Mono', monospace; color: var(--muted);">0%</span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" id="progress-bar-fill"></div>
          </div>
        </div>

        <label style="margin-bottom: 0.5rem; display: block;">Terminal de Ações</label>
        <div class="logs-terminal" id="logs-terminal">
          <div class="log-line">
            <span class="log-time">[00:00:00]</span>
            <span class="log-info">Painel Internacional carregado. Conecte seu WhatsApp e clique em Iniciar.</span>
          </div>
        </div>

        <div class="leads-table-container">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>País</th>
                <th>Nome</th>
                <th>WhatsApp</th>
                <th>Cidade</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="leads-tbody">
              <tr><td colspan="6" style="text-align: center; color: var(--muted);">Carregando leads...</td></tr>
            </tbody>
          </table>
        </div>

      </div>
    </div>
  </div>

  <script>
    const MSG_PT = "Olá, tudo bem? O meu nome é Leonardo, gostaria de falar consigo a respeito de uma proposta.";
    const MSG_BR = "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta.";

    function fillQuery(q, country) {
      document.getElementById('miner-query').value = q;
      document.getElementById('miner-country').value = country;
      const msgEl = document.getElementById('message-text');
      if (country === 'PT') {
        if (msgEl.value === MSG_BR || msgEl.value.trim() === '') {
          msgEl.value = MSG_PT;
        }
      } else if (country === 'BR') {
        if (msgEl.value === MSG_PT || msgEl.value.trim() === '') {
          msgEl.value = MSG_BR;
        }
      }
    }

    async function loadLeadsPreview() {
      const category = document.getElementById('category-select').value;
      const msgEl = document.getElementById('message-text');

      // Auto switch message template according to country
      if (category.endsWith('_pt')) {
        if (msgEl.value === MSG_BR || msgEl.value.trim() === '') {
          msgEl.value = MSG_PT;
        }
      } else if (!category.includes('pt') && category !== 'global_odonto' && category !== 'custom') {
        if (msgEl.value === MSG_PT || msgEl.value.trim() === '') {
          msgEl.value = MSG_BR;
        }
      }

      try {
        const res = await fetch(`/api/leads?category=${category}`);
        const data = await res.json();
        currentLeads = data.leads || [];
        renderLeadsTable({});
      } catch (e) {
        console.error("Erro ao carregar leads", e);
      }
    }

    async function mineCustomNiche() {
      const q = document.getElementById('miner-query').value.trim();
      const country = document.getElementById('miner-country').value;
      if (!q) {
        alert("Por favor, digite um nicho e cidade para minerar.");
        return;
      }

      const btn = document.getElementById('btn-mine');
      btn.disabled = true;
      btn.innerHTML = '<span>⏳ Minerando...</span>';

      try {
        const res = await fetch('/api/mine', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: q, limit: 25, country: country })
        });

        const data = await res.json();
        if (data.leads && data.leads.length > 0) {
          alert(`✔ Sucesso! Encontrados ${data.leads.length} leads sem site para "${q}".`);
          document.getElementById('category-select').value = 'custom';
          currentLeads = data.leads;
          renderLeadsTable({});
        } else {
          alert("Nenhum lead sem site encontrado para este termo exato. Tente outro termo ou cidade.");
        }
      } catch (e) {
        alert("Erro na mineração: " + e.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<span>🔍 Minerar Leads</span>';
      }
    }

    function renderLeadsTable(progressMap) {
      const tbody = document.getElementById('leads-tbody');
      tbody.innerHTML = '';

      const limit = parseInt(document.getElementById('limit-select').value) || 25;
      const visible = currentLeads.slice(0, limit);

      if (visible.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--muted);">Nenhum lead encontrado.</td></tr>';
        return;
      }

      visible.forEach((lead, idx) => {
        const status = progressMap[lead.name] || 'pending';
        let statusLabel = 'Pendente';
        let statusClass = 'tag-pending';

        if (status === 'sending') {
          statusLabel = 'Enviando...';
          statusClass = 'tag-sending';
        } else if (status === 'sent') {
          statusLabel = '✔ Enviado';
          statusClass = 'tag-sent';
        } else if (status === 'failed') {
          statusLabel = '✖ Falha';
          statusClass = 'tag-failed';
        }

        const isPt = lead.country === 'PT';
        const flag = lead.flag || (isPt ? '🇵🇹' : '🇧🇷');
        const countryClass = isPt ? 'pt' : 'br';

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${idx + 1}</td>
          <td><span class="country-tag ${countryClass}">${flag} ${lead.country_label || (isPt ? 'Portugal' : 'Brasil')}</span></td>
          <td><strong>${lead.name}</strong></td>
          <td style="font-family: 'JetBrains Mono', monospace; color: #38bdf8;">${lead.whatsapp}</td>
          <td style="color: var(--muted);">${lead.city_state || 'Geral'}</td>
          <td><span class="tag-status ${statusClass}">${statusLabel}</span></td>
        `;
        tbody.appendChild(tr);
      });
    }

    async function startAutomation() {
      const category = document.getElementById('category-select').value;
      const limit = parseInt(document.getElementById('limit-select').value) || 25;
      const interval = parseInt(document.getElementById('interval-slider').value) || 30;
      const message = document.getElementById('message-text').value.trim();

      if (!message) {
        alert("Por favor, digite uma mensagem de envio.");
        return;
      }

      try {
        const res = await fetch('/api/start', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            category: category,
            limit: limit,
            interval_seconds: interval,
            message_template: message
          })
        });

        if (!res.ok) {
          const err = await res.json();
          alert(err.detail || "Erro ao iniciar.");
          return;
        }

        document.getElementById('btn-start').disabled = true;
        document.getElementById('btn-pause').disabled = false;
        document.getElementById('btn-stop').disabled = false;

        if (!pollingInterval) {
          pollingInterval = setInterval(pollStatus, 1000);
        }
      } catch (e) {
        alert("Erro ao conectar com o servidor: " + e.message);
      }
    }

    async function togglePause() {
      try {
        const res = await fetch('/api/pause', { method: 'POST' });
        const data = await res.json();
        const btn = document.getElementById('btn-pause');
        if (data.status === 'paused') {
          btn.innerHTML = '<span>▶ Retomar</span>';
        } else {
          btn.innerHTML = '<span>⏸ Pausar</span>';
        }
      } catch (e) {
        console.error(e);
      }
    }

    async function stopAutomation() {
      try {
        await fetch('/api/stop', { method: 'POST' });
      } catch (e) {
        console.error(e);
      }
    }

    async function pollStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();

        const badge = document.getElementById('status-badge');
        const statusText = document.getElementById('status-text');
        badge.className = `status-badge ${data.status}`;

        const statusLabels = {
          idle: 'Pronto para Iniciar',
          starting: 'Abrindo Chrome...',
          waiting_qr: 'Aguardando Login WhatsApp (QR Code)',
          running: 'Enviando Mensagens...',
          paused: 'Pausado',
          stopped: 'Parado',
          completed: 'Concluído com Sucesso!',
          error: 'Erro na Execução'
        };
        statusText.textContent = statusLabels[data.status] || data.status;

        const qrBox = document.getElementById('qr-box');
        const qrWrapper = document.getElementById('qr-image-wrapper');
        if (data.status === 'waiting_qr') {
          qrBox.classList.add('active');
          if (data.qr_image) {
            qrWrapper.innerHTML = `<img src="${data.qr_image}" class="qr-img" alt="QR Code WhatsApp" />`;
          }
        } else {
          qrBox.classList.remove('active');
        }

        document.getElementById('stat-total').textContent = data.total_leads || currentLeads.length;
        document.getElementById('stat-sent').textContent = data.sent_count;
        document.getElementById('stat-fail').textContent = data.fail_count;
        document.getElementById('stat-timer').textContent = data.countdown > 0 ? `${data.countdown}s` : '0s';

        const total = data.total_leads || 1;
        const current = data.current_index;
        const pct = total > 0 ? Math.round((current / total) * 100) : 0;
        document.getElementById('progress-percent').textContent = `${pct}%`;
        document.getElementById('progress-bar-fill').style.width = `${pct}%`;

        if (data.current_lead) {
          document.getElementById('current-lead-text').textContent = `Enviando para [${current}/${total}]: ${data.current_lead}`;
        }

        const isBusy = ['starting', 'waiting_qr', 'running', 'paused'].includes(data.status);
        document.getElementById('btn-start').disabled = isBusy;
        document.getElementById('btn-pause').disabled = !isBusy;
        document.getElementById('btn-stop').disabled = !isBusy;

        if (data.leads_progress) {
          renderLeadsTable(data.leads_progress);
        }

        if (data.logs && data.logs.length > 0) {
          const term = document.getElementById('logs-terminal');
          term.innerHTML = data.logs.map(l => `
            <div class="log-line">
              <span class="log-time">[${l.time}]</span>
              <span class="log-${l.level || 'info'}">${l.msg}</span>
            </div>
          `).join('');
          term.scrollTop = term.scrollHeight;
        }

      } catch (e) {
        console.error("Erro no polling", e);
      }
    }

    // Init
    loadLeadsPreview();
    pollStatus();
    setInterval(pollStatus, 1500);
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    port = 5000
    print(f"Iniciando Servidor Web de Automação WhatsApp na porta {port}...")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
