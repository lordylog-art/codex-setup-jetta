---
name: templates-new-move
description: Reutilizar templates aprovados do New Move; conduzir Estúdio para composição nova ou protótipo solicitado.
---

# Templates New Move

## Ajuste em composição existente

Leia somente registro/componente/consumidores pertinentes em docs/templates-new-move.md e apps/web/src/app/templates. Reuse composição aprovada mais recente do contexto, respeitando observações e recusas posteriores. Correção funcional, texto, estado ou estilo pontual não exige novo Estúdio, inventário completo, alternativas, entrevista ou aceite repetido. Consulte Templates MCP uma vez se necessário para localizar decisão; contexto já resolvido basta.

Preserve componentes públicos, dados/handlers reais, validações, acesso por operação, foco/teclado, responsividade, tokens/transições. Exemplo/fixture não é integração. Confira superfícies/estados alterados e consumidores compartilhados. Skill de design adicional só para lacuna concreta, sem cascata obrigatória de routers/reviewers.

## Composição nova ou alteração material

Use templates-new-move-mcp/templates_context uma vez no principal. Compare opções pertinentes ao conteúdo. Apresente componente/preset, tamanho/apresentação/altura, posição/escala/imagem e motivo; confirme antes de implementar. Reuse aceite existente. Capacidade/template ausente: explique, marque “Não tem um template” e aguarde autorização específica, avançando nos itens compatíveis.

Estúdio completo apenas para protótipo solicitado ou grilling/grooming confirmado que o exija. Nesse caso leia as seções de prévia/alternativas/aceite de [SKILL.detalhado.md](SKILL.detalhado.md) e references/validacao-interativa.md. Preserve inventário do escopo, estados independentes, claro/escuro/mobile, feedback e controles previstos. Aceite enviado de todos os itens encerra Estúdio e autoriza implementação prevista; prototypeOnly encerra só escolha visual. Navegar/escolher sem enviar não aprova. Bot separado exige pedido explícito; executor não inicia bots recursivos.

## Padrões vigentes

- Visual do skeleton: linhas em cápsula, campos maiores com cantos arredondados e brilho neutro suave; evite blocos quadrados. Não altere a forma dos cards reais para estilizar o loading.

- Skeleton é padrão de conteúdo pendente em telas atuais e futuras: consulte `docs/skeletons-new-move.md` e reutilize `apps/web/src/components/operational-skeleton.tsx` no New Move. Escolha tabela com colunas reais, cards mobile, formulário ou detalhe conforme a região; preserve shell, títulos e filtros. Mantenha dados no refetch, erro/vazio/retry e feedback de salvar/importar. Use tokens sem bordas decorativas, status acessível sem controles fictícios e movimento reduzido. Cubra pendente→dados/erro e preservação em atualização nos testes nativos e Super QA pertinente. Em outro checkout, confirme os componentes disponíveis antes de aplicar.

- Menus: MenuAutomacoes/Ícones por assunto. Destrutivo vermelho, confirmar verde, atenção âmbar, consulta azul, impedido neutro com motivo acessível. Preserve ordem de domínio, callbacks, confirmação e permissões.
- Filtros simples: select nativo com estilos do catálogo, ProgramacaoFilterSelect quando compatível. Busca/multisseleção consulta capacidade existente.
- Modais: componentes do catálogo, AcoesModal e Jotinha raiz pequeno de busto (IMAGENS_JOTINHA). Pose pela ação/estado. Conteúdo denso amplia superfície/reduz imagem; mobile segue contrato. Dimensões/props vêm do registro/componente, sem duplicar tabelas aqui.
- Nova imagem só autorizada, referência canônica atual, identidade/roupa/recorte/fundo transparente e sem logos. Preserve escolhas recorrentes.
- Erros/loading/sync seguem AGENTS e componente. Segurança, retry/idempotência e autorização por operação permanecem.

Prévia não comprova backend nem autoriza produção/envios. Decisões/templateEvidence entregues alimentam aprendizado uma vez no marco; falha de gravação não vira aceite nem reabre prova válida. Protocolo detalhado sob demanda, não checklist de toda edição; este arquivo prevalece nas cerimônias.

## Limite da simplificação

A redução remove repetição de processo, não requisitos do produto. Preserve gates específicos de segurança/dados, prova real da fronteira alterada, aceites humanos de composição nova, testes exigidos pelo risco e autorizações de efeito externo. Não use esta política para marcar critério sem prova, alterar permissões, desligar proteção ou suprimir requisito do usuário.
