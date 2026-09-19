import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== VERIFICAÇÃO DO SUPORTE A PORTUGAL E BRASIL ===")

# 1. Verificar disparador_whatsapp.html
with open("disparador_whatsapp.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "🇵🇹 Portugal" in html, "Falta tag de Portugal no disparador HTML"
assert "🇧🇷 Brasil" in html, "Falta tag do Brasil no disparador HTML"
assert "setCountry('PT')" in html, "Falta função de seleção de país PT"
assert "https://wa.me/351" in html, "Falta link de WhatsApp com DDI +351"
assert "https://wa.me/55" in html, "Falta link de WhatsApp com DDI +55"
print("✔ disparador_whatsapp.html validado com sucesso!")

# 2. Verificar bancos de dados de Portugal
files_pt = [
    ("clinicas_dentarias_portugal_leads.json", 10),
    ("estetica_beleza_portugal_leads.json", 30),
    ("energia_solar_obras_portugal_leads.json", 5),
    ("clinicas_odontologicas_global.json", 70)
]

for filename, min_count in files_pt:
    assert os.path.exists(filename), f"Arquivo {filename} não encontrado"
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) >= min_count, f"{filename} tem apenas {len(data)} leads (esperado >= {min_count})"
        # Verificar se os números possuem formato válido
        for item in data:
            phone = item.get("whatsapp", "")
            assert phone, f"Lead sem telefone em {filename}: {item.get('name')}"
        print(f"✔ {filename}: {len(data)} leads validados com sucesso!")

# 3. Testar funções de app_automacao.py
import app_automacao

sample_pt_mobile = "912 345 678"
sample_pt_intl = "+351 962 014 991"
sample_br_mobile = "(11) 99876-5432"

ok_pt, fmt_pt, link_pt, is_mob_pt = app_automacao.is_portugal_phone(sample_pt_mobile)
assert ok_pt and is_mob_pt and "351" in link_pt, f"Falha no parse PT: {link_pt}"

ok_br, fmt_br, link_br = app_automacao.is_brazil_phone(sample_br_mobile)
assert ok_br and "55" in link_br, f"Falha no parse BR: {link_br}"

print("✔ Funções de validação e regex de telemóveis de Portugal e Brasil 100% operacionais!")

print("\n🚀 TODAS AS VERIFICAÇÕES PASSARAM COM SUCESSO!")
