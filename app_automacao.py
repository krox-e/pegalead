#!/usr/bin/env python3
"""
Servidor Web e Robô de Disparo 100% Automático no WhatsApp Web
Gerenciamento completo de sessão, QR Code ao vivo e disparos sem intervenção manual.
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
import uvicorn

sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI(title="Robô WhatsApp • Disparo 100% Automático")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".whatsapp_session")

# Global Automation State
STATE = {
    "status": "idle", # "idle", "connecting", "waiting_qr", "connected", "running", "paused", "stopped", "completed", "error"
    "is_connected": False,
    "qr_image": None, # Base64 data URL (PNG)
    "current_lead": None,
    "last_sent_lead": None,
    "current_index": 0,
    "total_leads": 0,
    "sent_count": 0,
    "fail_count": 0,
    "countdown": 0,
    "error_message": "",
    "logs": [],
    "leads_progress": {}
}

STATE_LOCK = threading.Lock()
STOP_EVENT = threading.Event()
PAUSE_EVENT = threading.Event()
RUNNER_THREAD: Optional[threading.Thread] = None

# Global Playwright Objects
PLAYWRIGHT_INSTANCE = None
BROWSER_CONTEXT = None
ACTIVE_PAGE = None
MANAGER_LOCK = threading.Lock()

def add_log(msg: str, level: str = "info"):
    timestamp = time.strftime("%H:%M:%S")
    entry = {"time": timestamp, "msg": msg, "level": level}
    with STATE_LOCK:
        STATE["logs"].append(entry)
        if len(STATE["logs"]) > 150:
            STATE["logs"].pop(0)
    print(f"[{timestamp}] {msg}", flush=True)

def ensure_browser_open():
    """Garante que o navegador Chromium/Chrome com a sessão do WhatsApp esteja aberto"""
    global PLAYWRIGHT_INSTANCE, BROWSER_CONTEXT, ACTIVE_PAGE
    from playwright.sync_api import sync_playwright

    with MANAGER_LOCK:
        if ACTIVE_PAGE is not None:
            try:
                ACTIVE_PAGE.title()
                return ACTIVE_PAGE
            except Exception:
                ACTIVE_PAGE = None
                BROWSER_CONTEXT = None

        if PLAYWRIGHT_INSTANCE is None:
            PLAYWRIGHT_INSTANCE = sync_playwright().start()

        if BROWSER_CONTEXT is None:
            add_log("Iniciando navegador com sessão persistente do WhatsApp...", level="info")
            os.makedirs(USER_DATA_DIR, exist_ok=True)
            
            # Try launching with channel='chrome', fallback to default chromium
            try:
                BROWSER_CONTEXT = PLAYWRIGHT_INSTANCE.chromium.launch_persistent_context(
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
            except Exception as e:
                add_log(f"Iniciando com Chromium integrado: {e}", level="info")
                BROWSER_CONTEXT = PLAYWRIGHT_INSTANCE.chromium.launch_persistent_context(
                    user_data_dir=USER_DATA_DIR,
                    headless=False,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage"
                    ],
                    ignore_default_args=["--enable-automation"],
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                )

            BROWSER_CONTEXT.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

        pages = BROWSER_CONTEXT.pages
        ACTIVE_PAGE = pages[0] if len(pages) > 0 else BROWSER_CONTEXT.new_page()
        return ACTIVE_PAGE

def qr_monitor_loop():
    """Thread em segundo plano que monitora login e captura o QR Code ao vivo"""
    global ACTIVE_PAGE
    try:
        page = ensure_browser_open()
        
        with STATE_LOCK:
            STATE["status"] = "connecting"
        add_log("Acessando WhatsApp Web para gerar QR Code...", level="info")
        
        if "web.whatsapp.com" not in page.url:
            page.goto("https://web.whatsapp.com", timeout=60000)

        for _ in range(120): # 4 minutes max
            if STOP_EVENT.is_set():
                break

            # 1. Check if already logged in (chats loaded)
            try:
                if page.locator('div[contenteditable="true"], div[data-tab="3"], #side, header, span[data-icon="chat"]').first.is_visible():
                    with STATE_LOCK:
                        STATE["is_connected"] = True
                        STATE["status"] = "connected"
                        STATE["qr_image"] = None
                    add_log("✅ WhatsApp Conectado e Autenticado com Sucesso!", level="success")
                    return
            except Exception:
                pass

            # 2. Check if QR expired and needs reload click
            try:
                refresh_btn = page.locator('button:has(span[data-icon="refresh"]), span[data-icon="refresh"], div[role="button"]:has(span[data-icon="refresh"]), button:has-text("Recarregar"), button:has-text("Reload")').first
                if refresh_btn.is_visible():
                    add_log("Recarregando QR Code expirado...", level="info")
                    refresh_btn.click()
                    time.sleep(2)
            except Exception:
                pass

            # 3. Check for QR Code canvas or container
            try:
                canvas = page.locator('canvas, div[data-ref], div[data-testid="qrcode"]').first
                if canvas.is_visible():
                    qr_bytes = canvas.screenshot()
                    b64 = base64.b64encode(qr_bytes).decode("utf-8")
                    with STATE_LOCK:
                        STATE["qr_image"] = f"data:image/png;base64,{b64}"
                        STATE["status"] = "waiting_qr"
                        STATE["is_connected"] = False
            except Exception:
                pass

            time.sleep(1.2)

    except Exception as e:
        add_log(f"Erro na conexão do WhatsApp: {e}", level="error")
        with STATE_LOCK:
            STATE["status"] = "error"
            STATE["error_message"] = str(e)

def execute_queue_dispatch(leads: List[Dict[str, Any]], default_template: str, interval: int):
    global ACTIVE_PAGE
    
    with STATE_LOCK:
        STATE["status"] = "starting"
        STATE["total_leads"] = len(leads)
        STATE["current_index"] = 0
        STATE["sent_count"] = 0
        STATE["fail_count"] = 0
        STATE["last_sent_lead"] = None
        STATE["error_message"] = ""
        STATE["leads_progress"] = {l.get("id", l.get("name", str(i))): "pending" for i, l in enumerate(leads)}

    add_log(f"🚀 Iniciando robô Playwright para {len(leads)} leads selecionados...", level="info")

    try:
        page = ensure_browser_open()
        if "web.whatsapp.com" not in page.url:
            page.goto("https://web.whatsapp.com")

        # Wait for login if not already logged in
        login_ok = False
        for _ in range(45):
            if STOP_EVENT.is_set():
                with STATE_LOCK:
                    STATE["status"] = "stopped"
                return
            try:
                if page.locator('div[contenteditable="true"], div[data-tab="3"], #side').first.is_visible():
                    login_ok = True
                    break
            except Exception:
                pass
            
            # Update QR code in case needed
            try:
                canvas = page.locator('canvas, div[data-ref]').first
                if canvas.is_visible():
                    qr_bytes = canvas.screenshot()
                    b64 = base64.b64encode(qr_bytes).decode("utf-8")
                    with STATE_LOCK:
                        STATE["qr_image"] = f"data:image/png;base64,{b64}"
                        STATE["status"] = "waiting_qr"
            except Exception:
                pass
            time.sleep(2)

        if not login_ok:
            add_log("Aguardando leitura do QR Code pelo celular antes de enviar.", level="warn")
            with STATE_LOCK:
                STATE["status"] = "waiting_qr"
            return

        with STATE_LOCK:
            STATE["qr_image"] = None
            STATE["is_connected"] = True
            STATE["status"] = "running"
        add_log("✔ Robô pronto! Iniciando envios 100% automáticos...", level="success")

        time.sleep(2)

        for idx, lead in enumerate(leads, 1):
            if STOP_EVENT.is_set():
                add_log("Disparos interrompidos pelo usuário.", level="warn")
                break

            while PAUSE_EVENT.is_set():
                with STATE_LOCK:
                    STATE["status"] = "paused"
                time.sleep(1)
                if STOP_EVENT.is_set():
                    break

            lead_id = lead.get("id", lead.get("name", str(idx)))
            name = lead.get("name", "Contato")
            phone = lead.get("whatsapp", "")
            country_flag = lead.get("flag", "📍")

            with STATE_LOCK:
                STATE["status"] = "running"
                STATE["current_index"] = idx
                STATE["current_lead"] = name
                STATE["leads_progress"][lead_id] = "sending"

            # Customized message
            msg = lead.get("mensagem_personalizada") or default_template
            msg = msg.replace("{nome}", name).replace("{empresa}", name).replace("{cidade}", lead.get("city_state", "")).replace("{bairro}", lead.get("bairro", ""))

            # Clean phone digits
            digits = "".join(filter(str.isdigit, phone))
            if digits.startswith("351") or digits.startswith("55"):
                pass
            elif len(digits) == 9 and digits.startswith("9"):
                digits = f"351{digits}"
            elif len(digits) in [10, 11]:
                digits = f"55{digits}"

            add_log(f"[{idx}/{len(leads)}] {country_flag} Enviando para: {name} ({phone})...", level="info")

            send_url = f"https://web.whatsapp.com/send?phone={digits}&text={quote(msg)}"

            try:
                page.goto(send_url)
                btn_selector = 'span[data-icon="send"], button[aria-label="Enviar"], button[aria-label="Send"], button[data-tab="11"], footer button:has(span[data-icon="send"])'
                page.wait_for_selector(btn_selector, timeout=30000)
                time.sleep(random.uniform(1.8, 2.5))
                
                # Click send button
                page.click(btn_selector)
                
                # Also press Enter as extra guarantee
                try:
                    page.keyboard.press("Enter")
                except:
                    pass
                    
                time.sleep(3.0)
                
                with STATE_LOCK:
                    STATE["sent_count"] += 1
                    STATE["last_sent_lead"] = lead
                    STATE["leads_progress"][lead_id] = "sent"
                
                add_log(f"✅ MENSAGEM ENVIADA AUTOMATICAMENTE para: {name} ({country_flag})!", level="success")

            except Exception as ex:
                with STATE_LOCK:
                    STATE["fail_count"] += 1
                    STATE["leads_progress"][lead_id] = "failed"
                add_log(f"⚠️ Não foi possível enviar para {name} (Número sem WhatsApp ou timeout).", level="warn")

            if idx < len(leads) and not STOP_EVENT.is_set():
                actual_delay = interval + random.randint(-1, 3)
                if actual_delay < 15:
                    actual_delay = 15
                
                add_log(f"⏳ Pausa de segurança anti-bloqueio ({actual_delay}s)...", level="info")
                
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

        add_log("🎉 Todos os disparos da fila foram finalizados!", level="success")

    except Exception as e:
        add_log(f"Erro na execução da automação: {str(e)}", level="error")
        with STATE_LOCK:
            STATE["status"] = "error"
            STATE["error_message"] = str(e)

# Request Models
class CustomQueueRequest(BaseModel):
    leads: List[Dict[str, Any]]
    message_template: Optional[str] = None
    interval_seconds: int = 30

class SingleLeadRequest(BaseModel):
    lead: Dict[str, Any]
    message_template: Optional[str] = None

# Routes
@app.get("/api/status")
def get_status():
    with STATE_LOCK:
        return JSONResponse(STATE)

@app.post("/api/connect_whatsapp")
def connect_whatsapp(background_tasks: BackgroundTasks):
    global RUNNER_THREAD
    STOP_EVENT.clear()
    background_tasks.add_task(qr_monitor_loop)
    return {"status": "connecting", "message": "Iniciando captura de QR Code..."}

@app.post("/api/dispatch_custom_queue")
def dispatch_custom_queue(req: CustomQueueRequest):
    global RUNNER_THREAD
    with STATE_LOCK:
        if STATE["status"] in ["running", "starting"]:
            raise HTTPException(status_code=400, detail="Automação já está em andamento.")

    STOP_EVENT.clear()
    PAUSE_EVENT.clear()

    target_leads = req.leads
    if not target_leads:
        raise HTTPException(status_code=400, detail="A fila de leads está vazia.")

    template = req.message_template or "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar a respeito de uma proposta."

    RUNNER_THREAD = threading.Thread(
        target=execute_queue_dispatch,
        args=(target_leads, template, req.interval_seconds),
        daemon=True
    )
    RUNNER_THREAD.start()

    return {"status": "started", "total_targets": len(target_leads)}

@app.post("/api/send_single_lead")
def send_single_lead(req: SingleLeadRequest):
    global RUNNER_THREAD
    with STATE_LOCK:
        if STATE["status"] in ["running", "starting"]:
            raise HTTPException(status_code=400, detail="O robô já está ocupado com outro envio.")

    STOP_EVENT.clear()
    PAUSE_EVENT.clear()

    lead = req.lead
    template = req.message_template or "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar a respeito de uma proposta."

    RUNNER_THREAD = threading.Thread(
        target=execute_queue_dispatch,
        args=([lead], template, 5),
        daemon=True
    )
    RUNNER_THREAD.start()

    return {"status": "started", "lead": lead.get("name")}

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

# Serve HTML
@app.get("/", response_class=HTMLResponse)
def index():
    html_path = os.path.join(os.path.dirname(__file__), "disparador_whatsapp.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>disparador_whatsapp.html não encontrado</h1>"

if __name__ == "__main__":
    port = 5000
    print(f"Iniciando Servidor Web do Robô de WhatsApp na porta {port}...")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
