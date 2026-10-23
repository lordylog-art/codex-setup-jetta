---
name: jetta-qa
description: Validar ERP Jetta com testes automatizados por persona, provas proporcionais de API/dados/componentes e navegador apenas para aparência ou lacuna demonstrada.
---

# Jetta QA

Priorize testes automatizados reproduzíveis por persona. Personas são atores, escopos e cenários de teste, não agentes nem sessões de cliques no ERP. Use o modo direto de entrega; Jetta Harness, flow.py, ledger e controller V2 não são dependências desta skill.

## Escolher a menor prova

1. Leia pedido/decisões atuais, diff e testes pertinentes. Reutilize provas válidas e fixtures existentes. Escolha o mecanismo que pode revelar o defeito; não crie plano/manifesto/relatório separado para uma verificação focal.
2. Comece pelos runners instalados: testes de função/serviço para regras, componentes para interações isoláveis, requests automatizados para API e banco isolado para persistência/migrations. Use scripts atuais do projeto; não adicione um framework ou runtime só para cumprir ritual.
3. Monte casos por persona relevante: ator autorizado executa o fluxo normal; ator de outro escopo tenta acesso direto; entrada inválida não produz escrita; rascunho/descarte conserva estado; gestores conferem filtro/total quando alterados. Consulte [estratégias](references/strategies.md) somente para casos pertinentes, não para gerar todas as personas/combinações.
4. Para autorização, teste permitir/negar no servidor com identidades/escopos distintos e ausência de dados/efeitos indevidos. Para persistência, salve e releia pelo mecanismo real. Mocks aceleram lógica local; não substituem a fronteira real alterada no aceite. Reutilize o mesmo percurso para vários critérios.

## Automação antes de navegador interativo

- Não abra ERP, CUA ou sessão de cliques por rotina para validar lógica que testes automatizados podem cobrir. Não navegue manualmente até um fluxo só para repetir um teste já válido.
- Quando comportamento nativo exigir browser (foco real, submit/navegação, providers ou cascata), prefira teste automatizado existente em headless, com asserções e fixtures. Isso não exige abrir uma janela interativa nem toda a aplicação se o componente real isolado reproduzir a fronteira.
- Use navegador interativo para inspecionar aparência ou uma lacuna concreta que a automação disponível não consiga observar. Antes, identifique essa lacuna em uma frase; uma falha de automação pede diagnóstico focal, não troca automática para cliques. Reuse preview, sessão e capturas válidas. Não reconstrua um E2E manual completo para conferir um modal.
- Mudança somente de lógica não exige Design Guardian/QA visual. Aparência alterada usa inspeção focal conforme [visual](references/visual.md) e Nosso Design; Impeccable somente quando houver decisão visual relevante. Aprovação humana só quando explicitamente exigida.
- Só inicie o runtime ERP quando a prova depender dele; siga [runtime](../jetta-local-runtime/SKILL.md) e AGENTS, incluindo instância isolada, efeitos externos desativados e acesso ADMIN próprio. [Segurança](references/safety.md) aplica-se às mutações reais. Não iniciar localhost para documentação/skills ou testes que dispensem servidor.

## Executar e concluir

Execute um lote coerente dos testes afetados e consolide os achados. Review independente segue risco e protocolo local; testes por persona não exigem um reviewer por persona. Depois de correção, repita apenas casos e impactos invalidados. Após duas tentativas equivalentes sem informação nova, mude hipótese/método; impedimento sem ação útil é registrado uma vez com condição de retomada.

Conclua com comando/interação, personas/casos cobertos, resultado e limitações no ticket/registro existente. PASS só para comportamento demonstrado; defeito confirmado é FAIL; prova necessária indisponível é BLOCKED/INCONCLUSIVE. Sugestões e cenários extras não ampliam o aceite. Pare quando os critérios pertinentes estiverem satisfeitos e os defeitos materiais resolvidos.

Para auditoria abrangente explicitamente solicitada, use [contratos](references/contracts.md), manifestos/helpers e estratégias combinatórias pertinentes. Fora desse modo, fórmulas, percentuais de orçamento, matrizes de personas, pairwise/3-way e relatórios formais são opcionais. CI, push, deploy, produção e envios externos continuam sujeitos à autorização específica.
