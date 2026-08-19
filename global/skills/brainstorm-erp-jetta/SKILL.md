---
name: brainstorm-erp-jetta
description: Brainstorm pratico para o projeto ERP Jetta/Jetta Move, gerando ideias priorizadas com top ranking, impacto operacional, custo tecnico, risco, quick wins e opiniao clara sobre o que vale ou nao vale a pena. Use quando o usuario pedir ideias, melhorias, priorizacao, roadmap, oportunidades de produto, automacoes, telas, fluxos, operacao de frota, SAC, programacao diaria, disponibilidade, Greenmile, roteirizacao, motoristas, ocorrencias ou decisoes sobre o que implementar no ERP atual.
---

# Brainstorm ERP Jetta

## Overview

Gerar ideias acionaveis para o ERP Jetta, sempre conectadas ao contexto real do produto: gestao operacional de frota, substituicao gradual de Google Sheets/Apps Script, Next.js/NestJS/PostgreSQL/Prisma, SAC, programacao diaria, disponibilidade, roteirizacao e integracao Greenmile.

Nao fazer brainstorm generico. Priorizar o que reduz retrabalho operacional, evita erro humano, melhora acompanhamento em tempo real, aumenta confiabilidade da base oficial na API/banco ou acelera decisoes de despacho/SAC.

## Contexto

Leia `references/project-context.md` no inicio, exceto quando a pergunta do usuario ja trouxer contexto suficiente e a resposta for claramente curta.

Quando o usuario estiver com uma tela aberta, considere a URL atual como sinal de contexto. Exemplo: `/clientes/3-coracoes/guarulhos/sac/carros-em-rota` indica foco em SAC, acompanhamento de frota, rotas em andamento, ocorrencias e visibilidade operacional.

Se precisar de mais precisao, inspecione arquivos do projeto antes de responder:

- `README.md`
- `apps/web/src/data/tres-coracoes-nav.config.ts`
- Rotas em `apps/web/src/app/clientes/3-coracoes/[unit]/...`
- APIs em `apps/web/src/app/api/...`
- Dominio operacional em `apps/api/src/modules/...`
- Schema em `apps/api/prisma/schema.prisma`

Evite ler arquivos enormes ou dumps SQL, especialmente `*.sql`, logs e `.next`.

## Workflow

1. Identificar o foco do pedido: produto inteiro, tela atual, fluxo operacional, UX, automacao, integracao, dados, seguranca ou performance.
2. Mapear dor operacional provavel: tempo perdido, baixa visibilidade, divergencia de dados, dependencias manuais, retrabalho, risco de atraso, atendimento ruim ou falta de rastreabilidade.
3. Gerar ideias em tres faixas:
   - Quick wins: baixo custo e impacto claro.
   - Apostas medias: exigem backend/estado/dados, mas destravam rotina.
   - Ideias grandes: alta alavancagem, maior risco, dependem de consolidacao de dados/processo.
4. Ranqueie por valor pratico, nao por criatividade. Use criterio:
   - Impacto operacional
   - Frequencia de uso
   - Urgencia do problema
   - Esforco tecnico
   - Risco de regressao
   - Dependencia de dados/integracoes externas
5. Diga explicitamente o que vale a pena, o que talvez valha depois, e o que nao vale agora.

## Formato De Resposta

Responder em portugues brasileiro, direto e opinativo. O usuario quer boas ideias com ranking e julgamento, nao uma lista neutra.

Use este formato quando o usuario pedir brainstorm amplo:

```text
Top ideias

1. Nome da ideia
   Vale a pena: Sim/Agora/Depois/Nao
   Por que: ...
   Impacto: Alto/Medio/Baixo
   Esforco: Baixo/Medio/Alto
   Risco: Baixo/Medio/Alto
   Primeiro passo: ...

2. ...

O que eu faria primeiro
...

O que eu nao faria agora
...
```

Para pedidos menores, entregue de 3 a 5 ideias. Para roadmap, entregue 8 a 12 ideias no maximo.

## Criterios De Valor

Favor forte para ideias que:

- Eliminam planilhas paralelas ou reconciliacao manual.
- Melhoram a confiabilidade da base oficial no banco/API.
- Reduzem tempo do SAC para saber onde esta cada carro, atraso, parada ou ocorrencia.
- Ajudam programacao e disponibilidade a decidir motorista/veiculo/carga com menos tentativa e erro.
- Mostram excecoes antes de mostrarem relatorios bonitos.
- Criam auditoria: quem alterou, quando, por que e qual impacto.
- Aproveitam dados ja existentes: cargas, motoristas, veiculos, rotas Greenmile, status de hidratacao, ocorrencias e disponibilidade.

Desfavoreca ideias que:

- Sao so cosmeticas enquanto o fluxo ainda e manual ou incerto.
- Dependem de IA sem dado confiavel suficiente.
- Criam painel executivo antes de resolver operacao diaria.
- Aumentam carga de cadastro manual sem retorno claro.
- Recriam regra critica em planilha ou frontend quando deveria estar no backend/API.
- Exigem integracao externa fragil sem fallback operacional.

## Saida Opinativa

Use frases claras:

- "Vale agora porque..."
- "Vale depois, quando..."
- "Nao vale ainda porque..."
- "Eu cortaria essa ideia por enquanto..."
- "O primeiro MVP deveria ser..."

Sempre inclua um "primeiro passo" implementavel, preferencialmente pequeno o bastante para virar uma tarefa com teste.

## TDD E Engenharia

Quando a ideia virar implementacao, lembrar a regra local: mudanca comportamental exige TDD decente. Sugira teste de regressao no nivel do fluxo real mais proximo, nao apenas helper isolado.

Para ideias de UI/estado/modal, recomende teste de interacao. Para API/auth/integracao, recomende contrato publico e caminho negativo relevante.
**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
