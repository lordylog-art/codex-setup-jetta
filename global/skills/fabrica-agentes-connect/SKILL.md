---
name: fabrica-agentes-connect
description: Criar, clonar, enriquecer e atualizar agentes de IA comuns da Connect Channels pela fábrica local tipada e pela sessão autenticada da extensão Chrome, incluindo perfil, objetivo, estágios, regras, habilidades e bases TABLE, QA ou FILE. Use quando o usuário pedir um novo agente, chamar informalmente esse agente de chatbot, adaptar um agente TESTE existente ou automatizar configurações da Connect sem Selenium. Também use para diagnosticar e parear a fábrica; só peça ao usuário o código quando um novo pareamento for realmente necessário.
---

# Fábrica de Agentes Connect

Usar a API local em `C:\Projetos\Jeta Move\tools\connect-agent-factory`. Não substituir esse fluxo por Selenium, chamadas arbitrárias à Connect ou edição visual.

## Preparação silenciosa

1. Executar `node scripts/factory-session.mjs status` a partir desta skill.
2. Tratar o resultado:
   - `READY`: guardar `controlCode` apenas para chamadas locais e continuar sem mencionar pareamento ao usuário.
   - `STOPPED`: executar `node scripts/factory-session.mjs start`.
   - `PAIRING_REQUIRED`: mostrar somente o `pairingCode`, pedir: “Cole este código na extensão Fábrica Connect, clique em Parear e responda ‘pareado’.” Pausar até a confirmação.
   - `RUNNING_CONTROL_UNAVAILABLE`: não matar o processo. Explicar que a API local já está rodando sem o código de controle recuperável e pedir autorização para reiniciá-la.
3. Depois de “pareado”, consultar `GET http://127.0.0.1:4317/v1/health`. Continuar apenas com `paired: true`.
4. Se a extensão não capturou a sessão da Connect, pedir apenas para abrir ou recarregar `https://app.connectchannels.com.br/ai`. Nunca pedir token, cookie ou header `Authorization`.

O código local não é uma chave da Connect. Não imprimi-lo quando a sessão já estiver pronta e não colocá-lo em arquivo versionado, log de auditoria ou resposta final.

## Identificar o artefato

- Tratar “agente”, “agente de IA” e o uso informal de “chatbot” como agente comum quando o pedido envolver Perfil, Objetivo, Estágios, Habilidades, Conhecimento e Configurações.
- Se o usuário pedir explicitamente um chatbot de automação com nós, grupos ou publicação, esta fábrica não cobre esse artefato. Usar a skill `criar-chatbot-connect` e manter o fluxo em rascunho.
- Não criar supervisor `isTeam=true` por esta fábrica enquanto o contrato local continuar restrito a agentes comuns.

## Criar um agente completo

1. Ler somente quando necessário:
   - `C:\Projetos\Jeta Move\tools\connect-agent-factory\README.md` para endpoints e estados;
   - `C:\Projetos\Jeta Move\tools\connect-agent-factory\SKILLS.md` para habilidades;
   - `C:\Projetos\Jeta Move\tools\connect-agent-factory\KNOWLEDGE.md` para bases.
2. Construir nome iniciado por `TESTE |`, com até 50 caracteres.
3. Criar primeiro as bases necessárias por `POST /v1/knowledge-plans`; aprovar e aguardar `COMPLETED` ou estado explícito de processamento.
4. Consultar `GET /v1/skills/catalog` e montar `blueprint.skills` tipado. Não usar `skillNames` quando houver configuração específica.
5. Criar `POST /v1/plans` com `creationMode: "FROM_SCRATCH"`, contexto técnico real, `GPT_4_1_MINI` quando solicitado e blueprint coerente.
6. Esperar `READY_FOR_APPROVAL`, conferir o diff sanitizado e aprovar pelo nome exato. A autorização do pedido para criar o agente basta para essa aprovação local; não pedir uma segunda confirmação salvo mudança material de escopo.
7. Aguardar um estado terminal. Nunca repetir automaticamente `CREATE_AGENT` ou `UPDATE_AGENT` após timeout ou resultado desconhecido.
8. Reler o agente e verificar nome, perfil, objetivo, estágios, regras, habilidades, bases, modelo e configurações. Tratar normalização da Connect separadamente de perda real de configuração.

## Atualizar um agente

- Aceitar somente agente comum cujo nome comece com `TESTE |`.
- Usar `POST /v1/update-plans` e preferir `changes.skillChanges` para preservar habilidades não mencionadas.
- Reler, conferir hash, revisar o diff, aprovar pelo nome exato e executar um único `PUT` tipado pela extensão.
- Em `UPDATED_UNVERIFIED`, não reenviar. Conferir por uma releitura ou pela interface autenticada antes de concluir.

## Habilidades e dependências

- Suportar os 11 tipos retornados pelo catálogo: calendário, follow-up, informações do contato, etiquetas, transferência, conclusão, card CRM, API, fluxo, campo do contato e MCP.
- Obter IDs reais da conta para campos, etiquetas, departamentos, painel e etapa do CRM. Nunca inventar ID para satisfazer validação.
- Se a fábrica ainda não possuir descoberta tipada para uma dependência, explicar a lacuna e pedir somente o identificador indispensável.
- Configurar `CALL_API` apenas com HTTPS e sem segredo. Não executar a URL durante criação ou edição.
- Manter autenticação MCP vazia. Se o servidor exigir segredo, orientar o usuário a configurá-lo diretamente na Connect; nunca transportar o segredo pelo localhost.
- Definir gatilho, idempotência, resposta esperada e falha explícita para habilidades externas.

## Gates de segurança

- Manter agente e chatbot em rascunho. Não publicar, arquivar, excluir, iniciar conversa, transferir atendimento, alterar contato, criar card real ou disparar habilidade sem autorização específica.
- Não expor credencial da Connect. A autorização permanece em `chrome.storage.session`.
- Não aceitar URL ou método arbitrário fora dos jobs tipados.
- Não mascarar `STALE`, `DUPLICATE`, `OUTCOME_UNKNOWN`, `CREATED_UNVERIFIED`, `UPDATED_UNVERIFIED` ou `FAILED`.
- Preservar português do Brasil com acentos corretos e verificar mojibake.

## Entrega

## Controle de operacao pendente

Antes de criar ou atualizar um plano, consultar `GET http://127.0.0.1:4317/v1/operations/active` com `x-factory-control`.

Quando o pedido atual autorizar substituir uma operacao pendente, cancelar o plano pelo endpoint correspondente: `POST /v1/plans/{id}/cancel`, `POST /v1/update-plans/{id}/cancel` ou `POST /v1/knowledge-plans/{id}/cancel`, enviando um motivo explicito. Nao cancelar operacao de outro escopo silenciosamente.

O cancelamento encerra somente a operacao e os jobs da fila local. Nao interrompe uma chamada externa ja iniciada pela extensao; o resultado posterior deve ser descartado pela fabrica e o plano tratado como `CANCELLED`.

Tratar `CANCELLED` como estado terminal local e informar quando ele tiver sido usado para liberar uma nova operacao.

Informar o ID, nome e link do agente, bases e habilidades configuradas, estado terminal observado e o que não foi executado. Não repetir o código de pareamento nem detalhes de sessão na resposta final.
