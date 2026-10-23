---
name: connect-channels-ai-agents
description: "Create or edit Connect Channels AI agents and supervisors over HTTP: profiles, models, stages, skills and knowledge. For \"Agentes Inteligentes\"; Builder flows use connect-channels-chatbots."
---

# Connect Channels — agentes de IA

Transforme o pedido em configuração nativa do módulo `/ai`. O Codex interpreta o pedido; a plataforma executa a IA com o provedor configurado na conta. Reutilize recursos e IDs existentes antes de criar empresa, credencial, agente ou conhecimento.

## Fontes e descoberta

Leia [contracts.md](references/contracts.md) antes de produzir um payload. Para habilidades, consulte [skills.md](references/skills.md); para arquivos/tabelas/FAQ, [knowledge.md](references/knowledge.md); para teste e integração, [testing-and-integration.md](references/testing-and-integration.md). O [mapa](references/architecture.md) explica o esquema completo recuperado. [evidence.md](references/evidence.md) separa pesquisa, REA, leitura real e operações ainda não executadas.

Contratos recuperados do editor publicado em 13/10/2026, não de um schema inventado. Material técnico: `C:/Users/caila/Documents/Codex/connect-channels-ai-agents`. Menu de modelos descreve opções do Connect; sua presença não garante acesso/capacidade no provedor. Preserve campos existentes fora da mudança solicitada.

## Conexão

O helper reutiliza `../connect-channels-chatbots/scripts/connect.mjs`: sessão Windows DPAPI, refresh e HTTP, sem browser. Execute os comandos a partir desta pasta. `CONNECT_ACCESS_TOKEN`, `CONNECT_SESSION_FILE` e `CONNECT_API_BASE_URL` seguem o cliente existente. Não confunda token público de integração com sessão autorizada para endpoints internos. `/core/v1/agent` cadastra usuário humano; agentes inteligentes usam `/ai/v1/aiagent`.

Tente a sessão salva em uma leitura antes de OTP. Se ausente ou refresh rejeitado por autenticação, siga a seção Conexão de [connect-channels-chatbots](../connect-channels-chatbots/SKILL.md) e seus helpers de autenticação. Rede/403/5xx pedem diagnóstico, não novo OTP. Nunca inclua tokens, chave de provedor ou headers de autenticação nos relatórios. O helper mascara segredos de leituras; edição recupera o objeto original em memória para preservar esses valores.

## Preparar e executar

1. Descubra a conta com `node scripts/agents.mjs catalog agents`, `companies`, `credentials` e `knowledge`. Resolva explicitamente empresa, credencial/modelos, equipes humanas e bases. Consulte a paginação completa. Distinga agente comum de supervisor pelo `promptConfig.isTeam`.
2. Defina nome/apelido, perfil, objetivo, passos ordenados, restrições, habilidades e conhecimento. Para supervisor, defina subagentes e resumos de triagem/transbordo. Pergunte apenas decisões de negócio ausentes; não escolha o primeiro ID automaticamente.
3. Prepare JSON nativo conforme contracts.md. Valide sem autenticação: `node scripts/agents.mjs plan <agent.json>`. Para edição, prefira patch dos campos pedidos: objetos mesclam; arrays fornecidos substituem a lista inteira, por isso inclua membros que devem continuar. O helper não promete validação integral do fornecedor.
4. Quando criar/editar estiver autorizado, use `create <agent.json> <journal-novo.json>` ou `update <id> <patch.json> <journal-novo.json>`. A solicitação de pesquisa ou geração local não autoriza mutação da conta. Save pode iniciar publicação do agente automaticamente; não ofereça um rascunho garantido. O serviço recuperado não possui um deploy separado de agente.
5. Confira readback campo a campo: objetivo, passos/ordem, restrições, skills/config/active/silêncio, empresa/credencial/modelos, teams/resumos, bases e transferências. Journal conclui em revisão de conteúdo necessária; não em aceite automático. Para confirmar compilação, releia `publishStatus` até READY/FAILED com prazo finito. READY não demonstra conversa correta.

## Retomada

Journal novo e exclusivo precede a escrita; ID retornado é registrado antes do readback. Timeout ou erro após tentativa mantém resultado incerto: `node scripts/agents.mjs reconcile <journal.json>` faz somente leituras. Reconcilie por ID e nome exato antes de qualquer repetição. Zero/uma/várias correspondências não autorizam retry automático nem adoção de agente alheio. Preserve o journal de origem.

Atualize por patch sobre leitura atual para conservar opções desconhecidas, inclusive configurações sensíveis. Snapshot mascarado serve à revisão, não à reconstrução de credenciais; não envie marcadores `[REDACTED]` como valores reais. Recursos vinculados podem estar em operação; identifique consumidores antes de editar/arquivar. Criar a skill não altera agentes, canais ou conversas existentes.

## Prova de conclusão

Separe: plano/validação local, autenticação/leitura, escrita/readback, compilação e comportamento da conversa. Testes locais do helper usam respostas simuladas; não provam fornecedor. `sandbox` e testes de conhecimento são chamadas de IA que podem consumir créditos e têm efeitos de ferramentas não comprovados: use o procedimento de testing-and-integration.md dentro do pedido autorizado.

Na demonstração de padaria em 14/10/2026 foram comprovados criação/edição e readback de agente, READY, upload/indexação de manual FILE e busca desse conteúdo no sandbox. Calendário respondeu no sandbox; CALL_API devolveu resultado simulado, sem consultar a URL. Entrega e resposta recebida no WhatsApp foram observadas, mas a execução integrada do agente ainda exige prova própria. Evidências: `C:/Users/caila/Documents/Codex/connect-channels-ai-agents/bakery-live-20261014`. Optimizer e demais habilidades continuam sem teste operacional.
