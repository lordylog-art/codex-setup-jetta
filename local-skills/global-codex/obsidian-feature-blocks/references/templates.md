# Formatos

Adapte conteúdo ao problema. Preserve informações obrigatórias; marque não aplicável com razão quando necessário. Não invente fatos para preencher campos.

## Origem

Preserve texto original em sua posição e propriedades. Acrescente/atualize seções da execução respeitando títulos existentes: 🎯 Objetivo; 👤 Usuários e fluxo; 📐 Regras de negócio; 📖 Vocabulário quando necessário; 🧠 Decisões consolidadas com razões; ❓ Dúvidas resolvidas (pergunta resumida e escolha; pendências separadas); 🚫 Fora de escopo; ⚠️ Restrições e observações; ✅ Escopo confirmado somente após confirmação.

## Proposta no chat

```markdown
# 🧩 Blocos sugeridos — Nome da Feature

## 🧱 Bloco 01 — Nome funcional
🎯 **Objetivo**
Resultado do estágio.

👀 **O que ficará visível/testável**
Capacidade executável e estado esperado.

🔧 **Inclui**
Escopo funcional e limites.

🧪 **Como validar**
Tela/comando, dados, passos e resultado.

🔗 **Dependências**
Nenhuma, ou blocos necessários.

---
```

Repita todos os blocos em cada versão negociada. Termine aguardando aprovação, sem materializar.

## Materialização

```text
<PROJECT_ROOT>/Blocos/<Nome da Feature>/
├── 00 - 🗺️ Visão Geral.md
├── 01 - 🧱 Nome funcional/
│   └── 01 - 🧱 Nome funcional.md
└── 02 - 🔌 Outro resultado/
    └── 02 - 🔌 Outro resultado.md
```

Quantidade e emojis dependem do problema: estrutura 🧱, UI 🎨, processamento ⚙️, regras 🧠, integração 🔌, comunicação 📨, dados 🗄️, segurança 🔐, validação 🧪, fechamento 🚀, observabilidade 📊, automação 🤖.

Windows: não use `< > : " / \\ | ? *`, caracteres de controle, nomes reservados (CON/PRN/AUX/NUL/COM1–9/LPT1–9, inclusive com extensão) ou ponto/espaço final. Nomes curtos respeitam o limite de caminho disponível. Sanitize somente nomes novos; confira colisões e contenção dentro de PROJECT_ROOT. Não renomeie existentes.

Reutilize propriedades existentes sem inventar schema de status. Wikilinks com caminhos verificados relativos ao vault: `[[Projetos/Projeto/Features/Origem|Origem]]`, `[[Projetos/Projeto/Blocos/Feature/01 - 🧱 Nome/01 - 🧱 Nome|Bloco 01]]`.

## Visão Geral

```markdown
# 🗺️ Visão Geral — Nome da Feature

## 🎯 Objetivo

## 📎 Especificação de origem
[[caminho real da SOURCE_NOTE|Nota original]]

## 🧩 Blocos
Links para todas as notas.

## 🔗 Ordem recomendada
Sequência e dependências reais.

## 🧠 Decisões fundamentais
Somente decisões que afetam múltiplos blocos; links para detalhes na origem.

## 🚫 Fora de escopo

## ✅ Definição global de pronto
Condições objetivas para concluir a feature inteira.
```

## Bloco

```markdown
# 🧱 Bloco XX — Nome

## 🎯 Objetivo
Resultado concreto.

## 👤 Resultado para o usuário
Capacidade que passa a existir.

## 👀 Estado observável ao final
O que visualizar/executar/testar e estado esperado.

## 📦 Escopo
### Inclui
### Não inclui

## 🧠 Regras de negócio deste bloco
Regras locais e links para decisões comuns.

## 🏗️ Direção técnica
Abordagem já definida, sem código linha a linha.

## 📂 Áreas provavelmente afetadas
Módulos/telas/serviços/tabelas/endpoints/workers/integrações/arquivos quando verificados. Distinga áreas conceituais de caminhos confirmados.

## 🔗 Dependências
### Depende de
### Libera
Links para blocos, ou Nenhuma.

## 🧪 Plano de validação
### Teste automatizado
Comportamento, entrada e sinal de aprovação; comando somente quando verificado.
### Teste manual
Tela/fluxo, permissões, pré-condições e dados; passos reproduzíveis.
### Resultado esperado
Prova de sucesso e falha relevante. Infra sem UI usa mecanismo observável concreto.

## ⚠️ Casos importantes
Somente aplicáveis: loading/vazio/erro/retry/duplicidade/concorrência/permissões/limites.

## 📊 Observabilidade
Sinais relevantes: logs/erros/métricas/tracing/health/auditoria, ou não aplicável com razão.

## ✅ Critérios de conclusão
- [ ] Resultado funcional disponível
- [ ] Critérios específicos mensuráveis atendidos
- [ ] Testes relevantes passando
- [ ] Fluxo principal validado na prática (ou mecanismo equivalente de infraestrutura)

## 🔗 Referências
Links reais para origem, Visão Geral e contexto necessário.
```

Checklists descrevem validações futuras; não marque concluído durante planejamento.
