# Imóvel Direto Monitor — Plano A (online)

Sistema web pronto para deploy com:
- login de administrador
- painel web
- filtros de busca
- cadastro/ingestão de anúncios
- classificação automática (`owner_likely`, `broker_likely`, `uncertain`)
- alerta por Telegram
- API pronta para conectar fontes permitidas depois

## Stack
- FastAPI
- Jinja2 + HTML/CSS
- SQLAlchemy
- SQLite local por padrão
- PostgreSQL compatível via `DATABASE_URL`

## Rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Abra:
- Painel: `http://127.0.0.1:8000/`
- Docs API: `http://127.0.0.1:8000/docs`

## Login padrão
Definido por variáveis de ambiente:
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`

## Deploy online

### Opção 1: Render / Railway / Fly.io
1. Suba este projeto em um repositório Git.
2. Configure as variáveis do `.env.example`.
3. Use o `Dockerfile` ou rode:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. Para produção, prefira PostgreSQL:
   - exemplo: `postgresql+psycopg://user:pass@host/dbname`

### Opção 2: VPS
```bash
docker build -t imovel-monitor .
docker run -p 8000:8000 --env-file .env imovel-monitor
```

## Principais rotas
### Web
- `GET /` dashboard
- `GET /login`
- `GET /filters/new`
- `GET /listings/new`

### API
- `POST /api/filters`
- `GET /api/filters`
- `POST /api/listings`
- `GET /api/listings`
- `POST /api/listings/{id}/recheck`

## Exemplo de ingestão de anúncio
```bash
curl -X POST http://127.0.0.1:8000/api/listings \
  -H 'Content-Type: application/json' \
  -d '{
    "source": "manual",
    "external_id": "post-001",
    "title": "Apartamento direto com proprietário na Mooca",
    "description": "Sem corretor. Vendo meu apto de 2 dormitórios.",
    "price": 430000,
    "neighborhood": "Mooca",
    "city": "São Paulo",
    "contact_name": "Carlos",
    "contact_role_hint": "owner",
    "url": "https://exemplo.local/anuncio/1"
  }'
```

## Como a classificação funciona
Heurísticas simples com score:
- favorece proprietário: “direto com proprietário”, “sem corretor”, “particular”, “sou o dono”, “meu imóvel”
- favorece corretor: “CRECI”, “consultor imobiliário”, “imobiliária”, “broker”, “corretor”
- penaliza repetição por mesmo contato ou padrão de linguagem muito comercial

## Próximos passos
- multiusuário
- WhatsApp Business / e-mail
- fila assíncrona
- NLP/LLM para classificação mais forte
- conectores externos autorizados
- revisão humana com feedback treinável

## Importante
Este projeto foi feito para a parte online do **Plano A**: painel + alertas + classificação + API de ingestão. A captação de dados do Facebook deve respeitar os canais e permissões autorizados da plataforma.
