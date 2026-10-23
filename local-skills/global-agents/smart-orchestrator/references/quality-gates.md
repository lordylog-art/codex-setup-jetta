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

Por critério: prova/veredito, origem/autor, base/candidato (SHA ou hash de conteúdo/diff sujo), comando/interação, resultado, ambiente/dependências/configuração não sensível e alcance/limitações. Reutilize só com equivalência verificável de código, ambiente, dependências/critério; viewport/tema/dados/estado/contexto importam no visual. Mudança invalidante reexecuta provas afetadas/impactos relacionados; preserve diagnóstico válido.

Typecheck, screenshot, HTTP 2xx, mock, teste focal ou commit isolados não certificam integração completa. Restrinja conclusão à superfície executada. Runner indisponível bloqueia prova; não confirma defeito do produto nem aprovação.

## Integração

Um titular integra com base atual conhecida, ownership preservado, dependências satisfeitas, conflitos resolvidos/gates válidos. Compare candidato revisado ao integrado; resolução alterada pede revisão/prova do delta. Preserve referências de commits/candidatos/revisões/validações.

Integre parcialmente quando seguro/autorizado; aceite final exige todos os critérios, inclusive prova integrada exigida. CI, deploy e ações externas requerem autorização. Sem mudança/falha/preocupação pendente, pare de ampliar/repetir testes após gates satisfeitos.
