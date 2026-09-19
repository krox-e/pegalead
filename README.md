# 🚀 PegaLead • Automação & Prospecção B2B de Leads no WhatsApp

Sistema completo e inteligente para **mineração, qualificação e prospecção de estabelecimentos comerciais no Google Maps sem website**, com disparo de mensagens 100% humanizado e seguro via WhatsApp no **Brasil 🇧🇷** e em **Portugal 🇵🇹**.

---

## 🌟 Funcionalidades Principais

1. **Mineração ao Vivo (Google Maps)**:
   - Extrai automaticamente empresas locais por nicho e cidade (ex: *clínicas dentárias em Lisboa*, *energia solar em São Paulo*, *estética no Porto*).
   - Filtra apenas empresas **sem website cadastrado** e com **WhatsApp verificado**.
   - Coleta notas de avaliação (estrelas), quantidade de reviews e endereço completo.

2. **Adaptação Linguística Automática (PT-BR & PT-PT)**:
   - 🇧🇷 **Brasil**: Mensagens personalizadas com padrão brasileiro (*"Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."*).
   - 🇵🇹 **Portugal**: Mensagens adaptadas para o português europeu (*"Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para a vossa clínica."*).

3. **Duas Formas de Utilização**:
   - 🌐 **Painel Web Interativo ([disparador_whatsapp.html](disparador_whatsapp.html))**: Interface standalone para disparar com 1 clique diretamente no navegador ou copiar mensagens.
   - 🤖 **Robô de Envio 100% Automático ([app_automacao.py](app_automacao.py))**: Servidor web com dashboard em tempo real, controle de cadência anti-bloqueio (25-35s) e envio via Playwright.

---

## 📁 Estrutura do Projeto

```
PegaLead/
├── app_automacao.py                       # Servidor Web FastAPI & Automação Playwright (localhost:5000)
├── disparador_whatsapp.html               # Painel Interativo de Prospecção (Brasil & Portugal)
├── prospector_maps.py                     # Extrator e minerador de leads via CLI
├── clinicas_dentarias_portugal_leads.json # Leads de Portugal (Odonto / Dentistas)
├── estetica_beleza_portugal_leads.json    # Leads de Portugal (Estética e Beleza)
├── energia_solar_obras_portugal_leads.json# Leads de Portugal (Energia Solar e Obras)
├── clinicas_odontologicas_leads.json      # Leads do Brasil (Odontologia)
├── saloes_de_beleza_leads.json            # Leads do Brasil (Salões de Beleza)
├── energia_solar_leads.json               # Leads do Brasil (Energia Solar)
├── vidracarias_leads.json                 # Leads do Brasil (Vidraçarias)
├── churrascarias_sem_site_100.json        # Leads do Brasil (Churrascarias)
├── .gitignore                             # Ignora sessões de WhatsApp e arquivos temporários
└── README.md                              # Documentação do projeto
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- Dependências: `fastapi`, `uvicorn`, `httpx`, `playwright`, `pydantic`

### 1. Instalação das dependências
```bash
pip install fastapi uvicorn httpx playwright pydantic
playwright install chrome
```

### 2. Iniciar o Painel de Automação (Localhost)
```bash
python app_automacao.py
```
Acesse no seu navegador: **[http://localhost:5000](http://localhost:5000)**

### 3. Mineração via Linha de Comando (CLI)
Para minerar leads diretamente pelo terminal:
```bash
# Prospecção no Brasil
python prospector_maps.py --country br --count 50

# Prospecção em Portugal
python prospector_maps.py --country pt --count 50
```

---

## 🛡️ Proteção Anti-Bloqueio do WhatsApp
- **Meta Diária Recomendada**: 25 a 30 envios por dia.
- **Intervalo de Segurança**: 30 a 60 segundos com variação humana randômica.
- **Formato Internacional**: Suporte nativo aos DDIs `+55` (Brasil) e `+351` (Portugal).

---

Desenvolvido com foco em alta conversão e eficiência em vendas B2B.
