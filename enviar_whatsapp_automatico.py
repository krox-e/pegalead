#!/usr/bin/env python3
"""
Robô de Envio Automático de Mensagens no WhatsApp Web
Desenvolvido para Leonardo realizar disparos seguros e automatizados para churrascarias.
"""

import json
import time
import sys
import os
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=" * 80)
    print(" 🤖 ROBÔ DE DISPARO 100% AUTOMÁTICO - WHATSAPP WEB • LEONARDO")
    print("=" * 80)
    
    # Check if playwright chromium is installed
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Erro: Playwright não está instalado. Execute com 'uv run --with playwright python enviar_whatsapp_automatico.py'")
        return

    # Load leads
    with open("churrascarias_sem_site_100.json", "r", encoding="utf-8") as f:
        leads = json.load(f)

    # Sort by review popularity
    for l in leads:
        try:
            l["reviews_int"] = int(str(l.get("reviews", 0)).replace(".", "").replace(",", ""))
        except:
            l["reviews_int"] = 0
    sorted_leads = sorted(leads, key=lambda x: x["reviews_int"], reverse=True)

    # Limit to 25 safe leads
    limit = 25
    target_leads = sorted_leads[:limit]

    user_data_dir = os.path.join(os.getcwd(), ".whatsapp_session")

    print(f"\nAlvo: {limit} churrascarias selecionadas com WhatsApp.")
    print("O navegador será aberto automaticamente na sua tela.")
    print("👉 Passo 1: Se for a primeira vez, escaneie o QR Code do WhatsApp no navegador.")
    print("👉 Passo 2: O robô enviará cada mensagem sozinho com intervalos seguros de 35 segundos.\n")

    with sync_playwright() as p:
        # Launch persistent browser context so session stays saved
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            channel="chrome", # Use installed Chrome if available, or Chromium
            args=["--start-maximized"]
        )
        page = browser.new_page()

        print("Conectando ao WhatsApp Web...")
        page.goto("https://web.whatsapp.com")

        print("\n⏳ Aguardando login no WhatsApp Web (escaneie o QR Code se necessário)...")
        # Wait until the main chat list or search bar appears
        try:
            page.wait_for_selector('div[contenteditable="true"], div[data-tab="3"], #side', timeout=120000)
            print("✔ WhatsApp Web conectado com sucesso!\n")
        except Exception:
            print("Tempo limite de login excedido. Tente novamente.")
            browser.close()
            return

        time.sleep(3)

        sucessos = 0
        falhas = 0

        for idx, lead in enumerate(target_leads, 1):
            name = lead["name"]
            phone = lead["whatsapp"]
            msg = lead["mensagem_personalizada"]
            
            # Clean phone digits
            digits = "".join(filter(str.isdigit, phone))
            if not digits.startswith("55"):
                digits = f"55{digits}"

            print(f"-----------------------------------------------------------------")
            print(f"[{idx}/{limit}] Enviando para: {name}")
            print(f"📱 Telefone: {phone} | 📍 {lead['city_state']}")

            send_url = f"https://web.whatsapp.com/send?phone={digits}&text={quote(msg)}"
            
            try:
                page.goto(send_url)
                
                # Wait for the Send button or text area
                # Selector for WhatsApp send button: span[data-icon="send"] or aria-label="Enviar"
                btn_selector = 'span[data-icon="send"], button[aria-label="Enviar"], button[aria-label="Send"]'
                page.wait_for_selector(btn_selector, timeout=25000)
                
                time.sleep(2) # Small human delay
                
                # Click send button
                page.click(btn_selector)
                print(f"✔ Mensagem enviada para {name} com sucesso!")
                sucessos += 1
                
                # Wait for message to actually dispatch
                time.sleep(3)

            except Exception as e:
                print(f"⚠ Não foi possível enviar para {name} (Número inválido ou timeout).")
                falhas += 1

            if idx < limit:
                interval = 35
                print(f"\n⏳ Pausa de segurança anti-bloqueio ({interval} segundos)...")
                for remaining in range(interval, 0, -5):
                    print(f"   Próximo envio em {remaining}s...", flush=True)
                    time.sleep(5)

        print("\n" + "=" * 80)
        print(f" 🎉 PROCESSO CONCLUÍDO!")
        print(f" ✔ Enviados com sucesso: {sucessos}")
        print(f" ✖ Falhas: {falhas}")
        print("=" * 80)
        
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    main()
