#!/usr/bin/env python3
"""
Disparador Semi-Automático de WhatsApp para Leonardo
Abre o WhatsApp Web para os Top 25/30 contatos com mensagem pré-preenchida
e intervalo seguro de tempo entre cada envio.
"""

import json
import time
import webbrowser
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=" * 80)
    print("      DISPARADOR SEGURO DE WHATSAPP • PROSPECÇÃO LEONARDO")
    print("=" * 80)
    
    with open("churrascarias_sem_site_100.json", "r", encoding="utf-8") as f:
        leads = json.load(f)

    # Sort by reviews
    for l in leads:
        try:
            l["reviews_int"] = int(str(l.get("reviews", 0)).replace(".", "").replace(",", ""))
        except:
            l["reviews_int"] = 0
    sorted_leads = sorted(leads, key=lambda x: x["reviews_int"], reverse=True)

    limit = 25
    top_leads = sorted_leads[:limit]
    
    print(f"\nForam selecionadas as {limit} churrascarias mais populares sem site.\n")
    print("Instruções:")
    print(" 1. Certifique-se de estar com o WhatsApp Web aberto no seu navegador.")
    print(" 2. O script abrirá a conversa com o texto já pronto para cada estabelecimento.")
    print(" 3. Você só precisará clicar em 'Enviar' no WhatsApp.")
    print(" 4. Entre cada contato, haverá uma pausa de segurança recomendada.\n")
    
    input("Pressione [ENTER] para iniciar o processo de disparo...")
    
    for i, lead in enumerate(top_leads, 1):
        print(f"\n-----------------------------------------------------------------")
        print(f"[{i}/{limit}] Abrindo: {lead['name']} ({lead['whatsapp']})")
        print(f"Cidade/UF: {lead['city_state']} | Avaliação: {lead['rating']} ★")
        print(f"Link: {lead['wa_link_com_mensagem']}")
        
        webbrowser.open(lead['wa_link_com_mensagem'])
        
        if i < limit:
            print(f"\n✔ Conversa aberta! Envie a mensagem no WhatsApp.")
            print(f"Aguardando 30 segundos de intervalo seguro para o próximo...")
            for remaining in range(30, 0, -5):
                print(f"  Próximo em {remaining}s...", flush=True)
                time.sleep(5)
                
    print("\n=================================================================")
    print(" 🎉 Todos os 25 contatos foram abertos com sucesso!")
    print("=================================================================")

if __name__ == "__main__":
    main()
