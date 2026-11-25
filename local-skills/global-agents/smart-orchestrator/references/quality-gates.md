# Qualidade e aceite

Resolva protocolos no catálogo instalado/regras do projeto; leia só skills relevantes. Não recrie Implement, Code Review, Design, QA visual, TDD ou segurança nem fixe caminhos de outro usuário. Fluxo especializado explicitamente escolhido mantém seu contrato; não misture automaticamente duas orquestrações.

| Risco | Superfície | Gate proporcional |
|---|---|---|
| Baixo | Local, reversível, sem impacto material em dados/acesso/contrato | Autoverificação focal; revisão adicional quando exigida. |
| Médio | Comportamento, componente compartilhado, estados/integração moderada | Autoverificação e revisão conjunta/independente conforme fronteiras, provas/regras. |
| Alto | Auth, integridade, migração, concorrência, finanças, segurança, contrato crítico/irreversibilidade | Provas do mecanismo real e revisões independentes necessárias; todos os gates. |

Incerteza material pede investigação ou gate superior. Autor se verifica antes do handoff. Independente é avaliador distinto do autor, com recorte/provas acessíveis; sem avaliador, etapa bloqueada, nunca renomeie autorrevisão como independente.

No ERP com `code-review`, preserve modos instalados, inclusive Standards/Spec independentes em alto risco. Outros projetos usam seu protocolo. Revisão procura defeitos/lacunas materiais; sugestão opcional não cria trabalho obrigatório.

Frontend usa ambiente isolado aprovado/componente real: comportamento, estados, geometria, responsividade/acessibilidade pertinentes. Contexto integrado/auth/provider exigido não é provado por story isolada. Preserve aprovação visual humana quando exigida. Backend prova autorização, segurança, persistência, concorrência, integridade/regressões alcançáveis.

## Validade e reutilização

- Atualize testes, fixtures e seletores junto com a mudança de comportamento. Antes de um lote caro, confira apenas os pré-requisitos pertinentes: build correto, readiness, autenticação e fluxo focal alterado.
- Teste o delta e suas regressões relacionadas primeiro. Execute a suíte ampla no marco de integração previsto, ou antes por risco compartilhado concreto; quantidade de tickets não exige suíte completa por ticket. Preserve exigências explícitas de QA e registro nos runners/agregado do projeto.
- Uma prova suficiente pode cobrir vários critérios. Após correção, repita falhas e impactos invalidantes; registre o motivo de ampliar o recorte. Mudança em autorização, isolamento, privacidade, persistência, migração, idempotência, concorrência ou custo mantém todas as provas reais e revisões pertinentes.
- No frontend, compare o primeiro recorte com a composição aprovada antes de replicá-lo. QA visual cobre controles, estados e superfícies atingidos; mudança exclusivamente de backend não cria rodada visual sem impacto demonstrado ou obrigação explícita. Preserve os gates visuais e humanos exigidos.
- Em IA, defina o corpus e a rubrica dos critérios cedo e exercite casos difíceis assim que o caminho real estiver disponível e autorizado. Reutilize roteiros e controle de custo revisados. Após falha, revalide o caso antes do corpus afetado; stub não fecha semântica real, e sucesso de execução não aprova conteúdo.

Por critério: prova/veredito, origem/autor, base/candidato (SHA ou hash de conteúdo/diff sujo), comando/interação, resultado, ambiente/dependências/configuração não sensível e alcance/limitações. Reutilize só com equivalência verificável de código, ambiente, dependências/critério; viewport/tema/dados/estado/contexto importam no visual. Mudança invalidante reexecuta provas afetadas/impactos relacionados; preserve diagnóstico válido.

Congele arquivos, dependências e artefatos que sustentam a prova, não todo o checkout por conveniência. Mudança concorrente exige avaliar impacto: preserve provas comprovadamente não atingidas e repita as invalidadas; dependência desconhecida pede investigação ou recorte maior. Nunca remova dependência relevante do manifesto para forçar PASS. Separe builds e recursos de teste antes da concorrência; não reconfigure a instância operacional para estabilizar testes.

Typecheck, screenshot, HTTP 2xx, mock, teste focal ou commit isolados não certificam integração completa. Restrinja conclusão à superfície executada. Runner indisponível bloqueia prova; não confirma defeito do produto nem aprovação.

## Integração

Um titular integra com base atual conhecida, ownership preservado, dependências satisfeitas, conflitos resolvidos/gates válidos. Compare candidato revisado ao integrado; resolução alterada pede revisão/prova do delta. Preserve referências de commits/candidatos/revisões/validações.

Integre parcialmente quando seguro/autorizado; aceite final exige todos os critérios, inclusive prova integrada exigida. CI, deploy e ações externas requerem autorização. Sem mudança/falha/preocupação pendente, pare de ampliar/repetir testes após gates satisfeitos.
