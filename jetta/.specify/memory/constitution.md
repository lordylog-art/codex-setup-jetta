# Constituição do ERP Jetta

Aplica-se ao Spec Kit. `AGENTS.md` continua sendo a regra operacional sempre carregada.

## Princípios

1. **Escopo e legado.** Basear a feature em evidência do ERP e aprovação do usuário. Preservar fluxos fora do escopo; não alterar contrato, regra, permissão, cálculo, fallback, limite ou semântica sem confirmação.
2. **Produção e dados.** Nenhuma alteração de serviço, produção, dados reais, segredo ou credencial sem autorização explícita para a ação específica. Diagnóstico read-only é permitido.
3. **Backend determinístico.** Decisões operacionais, cálculos e estados pertencem ao backend/banco. IA só interpreta linguagem ambígua, com entrada mínima e saída estruturada; nunca decide operação crítica.
4. **Economia de IA.** Usar o menor fluxo e modelo que preservem qualidade. Não reenviar contexto, produzir artefatos ou chamar revisões sem necessidade de risco. Registrar custo somente se houver medição disponível ou exigência do usuário.
5. **UI baseada em precedente.** Para UI administrativa, investigar a rota/tela mais próxima e reutilizar padrões. Para 3 Corações, aplicar a baseline de Guarulhos quando pertinente. Perguntar a composição de uma tela nova apenas quando a decisão não estiver evidente no escopo ou precedente.
6. **Validação proporcional.** Testar o comportamento e regressões plausíveis conforme risco; falhas não podem ser ocultadas. UI, segurança, contratos, integração e deploy exigem revisão específica somente quando afetados.
7. **Rastreabilidade mínima útil.** Feature completa deve ligar requisito, decisão, task e evidência. Use os artefatos já existentes; crie arquivos adicionais apenas se eles resolverem uma necessidade concreta de retomada ou auditoria.
8. **Segredos e linguagem.** Proteger dados sensíveis e manter texto humano em português do Brasil correto.

## Gates humanos

Pausar apenas para decisão material de produto/UX, ambiguidade que altere escopo ou contrato, migração/destruição de dados, operação externa, credencial/ambiente, deploy/restart ou falha sem correção comprovada. Perguntas devem ser objetivas e agrupadas em até cinco.

## Fluxo Spec Kit

1. Descobrir apenas os precedentes e contratos afetados.
2. Registrar escopo, impactos, decisões pendentes e aceite de forma proporcional.
3. Planejar e dividir tasks somente quando a complexidade justificar.
4. Implementar com diff mínimo e validar a superfície afetada.
5. Reportar evidências, pendências e riscos reais.

Exceções exigem aprovação explícita, motivo e impacto. Esta Constituição prevalece sobre templates e skills Spec Kit; em conflito com regras operacionais, prevalecem segurança e autorização.

**Versão**: 2.0.0 | **Última alteração**: 2026-08-19
