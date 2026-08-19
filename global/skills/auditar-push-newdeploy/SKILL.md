---
name: auditar-push-newdeploy
description: Auditar commits locais da branch main que já foram commitados e ainda não receberam push no ERP Jetta, verificar se o NewDeploy.ps1 consegue publicá-los com baixo risco, incluindo migrations pendentes e o gate antecipado do Prisma, pedir autorização antes de executar somente o push e, quando houver incompatibilidade, explicar os bloqueios e oferecer uma correção mínima. Usar quando o usuário perguntar se os commits sem push podem subir pelo NewDeploy, se o deploy novo dará conta das mudanças, se migrations impedirão o build/cutover, se é tranquilo dar push, ou pedir para corrigir o que impede esse deploy.
---

# Auditar Push para NewDeploy

## Limite da skill

Auditar e, após autorização explícita, executar apenas o `git push` da `main`. Nunca executar deploy, SSH, `git pull`, migration, alteração de ambiente, Caddy, PM2 ou restart de serviço. O usuário fará o deploy manualmente.

Não prometer ausência absoluta de erros. Dar parecer de baixo risco somente com evidência local suficiente e declarar qualquer validação que não pôde ser feita.

## Etapa 1 — Auditar commits sem push

1. Trabalhar somente no repositório `C:\Projetos\Jeta Move` e na branch `main`. Não criar nem trocar de branch.
2. Atualizar a referência remota com `git fetch origin main`. Se falhar, parar: não usar uma referência remota possivelmente desatualizada como se fosse atual.
3. Coletar:
   - `git status --short --branch`;
   - upstream configurado;
   - contagem ahead/behind;
   - `git log --oneline @{u}..HEAD`;
   - `git diff --stat @{u}..HEAD`;
   - `git diff --name-status @{u}..HEAD`;
   - diffs relevantes do mesmo intervalo.
4. Se não houver upstream ou commits à frente, informar objetivamente e não oferecer push.
5. Se a branch estiver atrás ou divergente, classificar como não apta. Não executar pull, merge ou rebase sem pedido explícito.
6. Separar alterações não commitadas. Elas não entram no push e não devem ser confundidas com o intervalo auditado. Não modificar, incluir nem descartar arquivos do usuário.
7. Verificar secrets, `.env` real, dumps, exports, backups, logs, dados reais e arquivos `.sql` fora de `apps/api/prisma/migrations/**/migration.sql`. Usar `hacker-safado` antes de autorizar qualquer push quando aplicável.

## Etapa 2 — Conferir compatibilidade com o NewDeploy

Ler o `NewDeploy.ps1` atual, `tools/newdeploy-zero-downtime.tests.ps1` e, quando existir, `tools/newdeploy-migration-gate.tests.ps1`; não presumir comportamento pela memória.

### Visão obrigatória sobre migrations

1. Separar três perguntas que não são equivalentes:
   - a migration está versionada e o SQL é compatível com blue/green?;
   - o banco remoto já aplicou a migration?;
   - o comando manual de deploy incluirá a autorização explícita necessária?
2. Tratar o banco remoto como fonte de verdade para migrations aplicadas. A auditoria local não pode afirmar que o banco está alinhado sem evidência remota; como esta skill não acessa a VPS, registrar essa pré-condição como não validada.
3. Reconhecer o gate atual do `NewDeploy.ps1`: sem `-AllowBlueGreenMigrations`, ele executa `prisma migrate status` no workspace isolado antes de TypeScript/build. Qualquer código de saída não saudável bloqueia cedo por migration pendente, histórico divergente, migration falha ou conexão indisponível.
4. Não classificar esse bloqueio antecipado como defeito nem sugerir removê-lo, ignorá-lo, transformar erro em aviso ou criar fallback. A correção deve ser na migration/ambiente ou na execução manual consciente com a opção explícita.
5. Não usar somente o intervalo Git como prova de que não há migration pendente. Em uma nova tentativa depois de um pull ou deploy falho, `HEAD` pode já conter a migration e o diff atual ficar vazio; o status do Prisma continua sendo a proteção efetiva.
6. Quando houver migration no intervalo auditado, classificar o deploy como `apto condicionado`, nunca como apto irrestrito: exigir deploy completo, revisão do SQL e `-AllowBlueGreenMigrations`. O push pode ser apto mesmo com essa condição, desde que ela seja declarada antes da autorização.

Classificar os arquivos e o trabalho necessário:

- Apenas `apps/api/src/**`, `apps/web/src/**`, `apps/web/public/**` e `.requirements/**`: avaliar o modo `-Fast` e suas guardas reais.
- `package.json` ou lockfile: confirmar que o deploy completo instala dependências e recompila os apps afetados; o modo rápido não é apto.
- Prisma/schema/migrations: exigir migration versionada, revisar SQL e compatibilidade entre versão antiga e nova. Só considerar apto condicionado para blue/green quando a migration for aditiva, reversível na prática e compatível com ambas as versões; registrar que o deploy manual precisará de `-AllowBlueGreenMigrations`. Avaliar também lock de `CREATE INDEX`, criação/validação de FK e volume da tabela. Drop, rename, mudança destrutiva, backfill pesado ou lock relevante bloqueiam o parecer.
- `.env.example` ou nova variável: confirmar que a variável estará configurada na VPS pelo fluxo seguro antes do cutover. Nunca ler nem expor valores secretos. Pendência de ambiente bloqueia o parecer.
- `NewDeploy.ps1`, Caddy, portas, PM2, infraestrutura, scripts operacionais, autenticação, contratos compartilhados ou múltiplos serviços: revisar especificamente a superfície afetada e exigir validação focada; não declarar apto por heurística de caminho.
- Schema alterado sem migration, segredo/dado real, contrato incompatível, erro conhecido ou pré-condição remota não satisfeita: bloquear.

Executar somente validação local e não destrutiva, proporcional ao diff:

- analisar sintaxe do `NewDeploy.ps1` sem executá-lo;
- rodar `tools/newdeploy-migration-gate.tests.ps1` quando existir e migrations ou o gate forem afetados;
- rodar `tools/newdeploy-zero-downtime.tests.ps1` quando o deploy ou suas guardas forem afetados;
- localizar e rodar testes focados dos apps alterados quando forem necessários para sustentar o parecer;
- não rodar suíte completa automaticamente;
- nunca mascarar falha nem afirmar que uma validação passou sem executá-la.

## Etapa 3 — Responder com uma decisão

### Apto

Usar esta conclusão quando o intervalo está entendido, não há divergência nem dado sensível, as pré-condições estão satisfeitas, o NewDeploy cobre o trabalho e as validações necessárias passaram:

```text
Sim, é tranquilo: o NewDeploy cobre estas mudanças pelo modo <rápido/completo>, com <resumo curto das condições>. Quer que eu execute o push da main?
```

Antes da pergunta, listar brevemente commits, arquivos relevantes, modo esperado e validações executadas. Não executar o push na mesma resposta.

Quando houver migration compatível, usar conclusão condicional explícita, por exemplo:

```text
O push está apto, mas o deploy é condicionado: deve ser completo e executado manualmente com -AllowBlueGreenMigrations após revisar o SQL. Sem essa opção, o NewDeploy bloqueará antes do build, como esperado. Quer que eu execute o push da main?
```

### Não apto

Usar esta conclusão quando houver qualquer bloqueio ou evidência insuficiente:

```text
Não, o NewDeploy não cobre estas mudanças com segurança porque: <motivos concretos>. Quer que eu corrija isso?
```

Apontar a menor correção possível. Não alterar código antes do “sim”. Se a correção mudar regra de negócio, contrato, dados, ambiente real ou exigir downtime, explicar o impacto e pedir confirmação específica.

## Etapa 4A — Push autorizado

Interpretar o “sim” conforme a última pergunta feita. Se a última pergunta foi sobre push:

1. Repetir `git fetch origin main` e confirmar que `HEAD`, upstream e intervalo auditado não mudaram.
2. Se algo mudou, refazer a auditoria e pedir autorização novamente.
3. Executar a checagem final de segredo/dump.
4. Executar somente `git push origin main`.
5. Confirmar o commit enviado e encerrar. Não iniciar o NewDeploy nem acessar a VPS.

## Etapa 4B — Correção autorizada

Interpretar o “sim” como autorização de manutenção somente se a última pergunta foi “Quer que eu corrija isso?”. Então:

1. Corrigir apenas os bloqueios listados, com alteração cirúrgica e sem refatoração paralela.
2. Seguir as regras e skills de implementação do projeto, incluindo TDD/revisão quando aplicáveis.
3. Preservar comportamentos e contratos fora do escopo.
4. Executar validações focadas e revisar o diff.
5. Criar o commit local obrigatório na `main`, sem push.
6. Refazer uma única vez a auditoria completa dos commits sem push.
7. Se ficar apto, voltar à pergunta de autorização do push. Se continuar bloqueado, parar e relatar o diagnóstico; não entrar em loop de correções.

## Formato da entrega

Manter a resposta curta, mas sempre informar:

- commits auditados;
- modo do NewDeploy aplicável;
- decisão e motivos;
- validações executadas e não executadas;
- alterações não commitadas excluídas do push;
- a pergunta exata de autorização correspondente à próxima ação.
