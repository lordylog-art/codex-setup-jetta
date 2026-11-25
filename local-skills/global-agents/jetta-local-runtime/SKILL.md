---
name: jetta-local-runtime
description: Ligar, reutilizar ou diagnosticar o localhost do ERP Jetta/New Move pelo MCP e entregar acesso ADMIN humano autenticado. Use quando a tarefa depender da API, Web, PostgreSQL ou login desse ERP.
---

# Localhost do Jetta pelo MCP

Use somente quando o usuário pedir o ERP ligado ou o trabalho depender dele em execução. Documentação, skills e testes isolados dispensam runtime; outros aplicativos usam seus próprios fluxos.

## Fluxo padrão para todos os chats

1. Reutilize o contexto já resolvido de `AGENTS.md` e determine a raiz do checkout solicitado (principal neste PC: `D:/newmove`). Use primeiro o servidor MCP `jetta-local-runtime`:
   - Para ligar/reutilizar uma instância com autorização do pedido: `jetta_local_start({project: "D:/newmove", authorized: true})`.
   - Para consultar sem iniciar: `jetta_local_status({project: "D:/newmove"})`.
   - Em `STARTING`, respeite `retryAfterMs` e consulte status; outra chamada de start é desnecessária. Em `BLOCKED` ou `FAILED`, investigue a causa antes de repetir. O MCP reutiliza o launcher rápido, verifica o repositório/checkout e coordena partidas concorrentes.

2. Em `READY`, siga o objeto `authentication` no navegador do usuário, preferindo o interno quando não houver preferência explícita. Reutilize a sessão do host exato e confira `/api/auth/me`. Confirme a conta humana esperada e papel `ADMIN`; no checkout principal, a conta humana já usada é `a@a.com`.
   - Se faltar sessão, faça login pelo formulário existente com as credenciais humanas autorizadas disponíveis e **Manter conectado**. Guarde credenciais em fonte privada autorizada, nunca nesta skill ou na chamada MCP. Se não houver sessão nem credencial disponível, peça apenas o dado que falta.
   - `READY` comprova o runtime, não o login humano. `SEED_ADMIN_*`, `TEST_LOGIN_*`, `-WithCodexBrowser`, `/api/auth/codex/*` e state Playwright não substituem a sessão humana.
   - Um novo login por senha pode invalidar a sessão anterior da mesma conta. Faça a entrega humana por último e preserve-a, sem login posterior em runner.

3. Confirme a página real carregada, mantenha a aba aberta (marque-a como entregável quando necessário) e entregue a URL clicável, saúde e identidade resumida. Deixe o runtime ligado. Evite novas instalações, limpezas de cache, QA global e benchmarks para uma simples abertura.

## Falha e fallback

- `BLOCKED` não significa MCP indisponível nem autoriza contornar suas proteções por shell. Logs são privados; leia só os caminhos/etapas pertinentes, protegendo valores de env, cookies, tokens e senhas. Coordenação incerta pede reconciliação de ownership.
- Se a ferramenta ainda não estiver disponível em um chat aberto, reconecte os MCPs ou use um novo chat quando possível. Apenas se o MCP estiver de fato indisponível, siga o launcher oficial no checkout: remova `JETTA_RUNTIME_ENV` e `JETTA_LOCAL_FROZEN_SOURCES` herdados do processo, consulte `npm run status` e execute `npm start` somente se parado. Repita as remoções em cada novo shell. Em D:/newmove, preserve o ambiente privado resolvido pelo launcher, sem forçar `.env` legado. Configurações explícitas de outras instâncias seguem seu `AGENTS.md`.
- Leia `docs/local-runtime.md` do checkout somente para configuração, recuperação ou detalhes do MCP. Não use fontes congeladas como atalho; preserve a recarga automática. Não mate processos por porta, remova lease/lock ou recrie dados por tentativa.
- Preserve banco, arquivos, credenciais, permissões, ativações, integrações e agendas configuradas. O MCP não para/recria instâncias nem concede autorização para produção, VPS, deploy, push, CI ou novos envios externos.
