---
name: new-move
description: Use when planning or implementing New Move transitions, operation-scoped screens/actions, reusable templates, or their mandatory Admin automation and schedule configuration.
metadata:
  short-description: New Move
---

# New Move

Use este contexto ao trabalhar na transição do Move para uma base central, escalável e multioperação. Leia [o contexto completo da migração](../../../docs/move-central-migration.md) antes de alterar telas, navegação, dados por CC ou automações.

Regras de trabalho:

- Confirme a worktree, branch, estado de integração e rotas presentes antes de assumir que `/templates` ou uma tela migrada está disponível. Candidatos em worktrees isoladas e arquivos `.scratch` não comprovam integração.
- Reutilize os templates compartilhados do Move quando estiverem disponíveis na base autorizada; não replique telas legadas por operação.
- Preserve regras de negócio, scripts, integrações e automações que ainda tenham uso. Remova uma regra somente quando o escopo pedir e seus efeitos/consumidores estiverem compreendidos.
- Mantenha operação/CC explícito em dados e ações. A autorização é server-side; interface, rota antiga, cliente ou marca não concedem acesso.
- Isole listas, cargas, filtros, menus flutuantes, barras de ação e automações pelo CC selecionado. Preserve acesso e contexto ao alternar operações.
- Integrações existentes: reutilize os vínculos e credenciais já configurados; preserve ativações autorizadas após reiniciar e valide operações reais na API do runtime.
- Feedback operacional: use os templates padrão no contexto da ação. Mantenha a barra de ferramentas livre de avisos técnicos fixos de configuração; corrija a causa sem mascarar falhas ou conceder acessos.
- Faça mudanças por fluxo, respeite consumidores legados ainda ativos e valide o comportamento real afetado.
- Em toda UI alterada, execute [Jetta QA](C:/Users/caila/.agents/skills/jetta-qa/SKILL.md), incluindo a persona [Front-end enjoado](C:/Users/caila/.agents/skills/jetta-qa/references/visual.md): adequação do template ao conteúdo real, pixels inspecionados, interações, celular/tablet/desktop e temas claro/escuro. Template existente e testes verdes não aprovam acabamento; siga a confirmação de composição exigida por AGENTS antes de editar a interface.
- Esta skill fornece contexto, não autorização para CI, push, deploy, produção, integração de worktrees ou envios externos.

## Administração obrigatória em cada transição

Ao migrar ou adicionar uma tela, ação ou automação, inclua sua configuração em **Administração > Operações** (`/admin/visibilidade`) na mesma entrega. Leia a seção “Administração das transições” do [contexto da migração](../../../docs/move-central-migration.md) e confirme os contratos presentes na base autorizada.

1. Inventarie telas, ações, automações e rotinas periódicas do fluxo New Move. Registre as capacidades no catálogo do servidor e no catálogo explícito do Admin; defina as operações/CCs suportadas. Use nomes de ações compreensíveis, como “Enviar mensagens do chatbot” ou “Preencher planilha”, com descrição do efeito e do local de configuração.
2. Reutilize as quatro abas: **Módulos** para acesso às telas; **Automações** para disponibilidade das ações por operação; **Sincronizações automáticas** para consultas periódicas existentes; **Agendamentos** para dias, horário/janela e ativação das rotinas de negócio. Apresente somente fluxos New Move; ocultar legado não autoriza parar suas execuções nem apagar configurações/histórico.
3. Mantenha uma única configuração por rotina/operação. Se a sincronização já tem editor, Agendamentos deve abrir essa configuração existente. O scheduler/worker deve consumir o estado salvo no painel e aplicar a mesma autorização server-side da ação manual; cadastrar apenas um checkbox visual não conclui a transição.
4. Preserve credenciais, vínculos, horários, dias e ativações já salvos, inclusive em migrações, QA e reinícios. Configurações novas começam desativadas para revisão, sem conceder grants ou ativar envios automaticamente. Ativação por operação pertence ao painel, não a novas flags por unidade no .env; credenciais e controles globais explícitos continuam protegidos.
5. Reutilize Template Mãe, editores e modais existentes. Mostre a unidade/CC selecionada e o motivo de indisponibilidade. Use Brasília; rotinas diárias têm um horário e dias, e rotinas por intervalo preservam a frequência existente, com janela, dias e ativo editáveis. Processadores internos de filas permanecem fora do painel.
6. Valide nas unidades afetadas: aparecer na aba correta, editar/salvar/reler, trocar unidade sem vazamento, preservar rascunhos e agendas anteriores, rejeitar falta de permissão e configuração inválida e comprovar que a execução respeita a configuração salva. Use processos próprios para testes simulados; mantenha as integrações configuradas do localhost funcionando. Registre a evidência e os limites, sem disparos externos de teste sem autorização específica.
