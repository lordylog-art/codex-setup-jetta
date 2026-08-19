---
name: modal-operacional
description: Criar, editar ou revisar modais operacionais do ERP Jetta no padrão visual da programação/alocação manual, com header azul full-bleed, corpo claro, cards internos, borda laranja de destaque, campos settings-field/settings-input, botões padronizados e validação visual/funcional focada.
---

# Modal Operacional

Use esta skill quando o usuário pedir para criar, ajustar, redesenhar ou padronizar modais no ERP Jetta, especialmente quando mencionar: modal de programação, modal de alocação manual, trocar motorista, registrar senha, ocorrências, SAC, header azul, padrão de cores, SVG personalizado, botão de fechar ou campos/botões no mesmo estilo.

## Princípios

- Faça mudança cirúrgica: CSS/markup do modal, sem refatorar fluxo.
- Preserve contrato, estado, callbacks e payloads existentes.
- O modal deve parecer ferramenta operacional, não landing page.
- Header azul deve cobrir 100% do topo do modal, sem parecer um card interno.
- Corpo deve usar fundo `#f7faff`, com cards brancos e bordas `#dbe5f1`.
- Destaques estruturais usam laranja `#f57c20`, normalmente em borda esquerda ou bullets.
- Campos usam `settings-field`, `settings-label`, `settings-input` e `settings-select`.
- Botão de fechar no header usa SVG de X dentro de botão branco, classe `sac-export-modal__close`.
- Botões de ação usam padrões existentes: secundário com `admin-btn-secondary`; confirmação com `programacao-confirm-dialog__confirm` quando for ação positiva.

## Workflow

1. Localize o modal existente e compare com modal de referência da programação/alocação manual.
2. Verifique classes globais que podem limitar tamanho, principalmente `.admin-dialog`, `.programacao-feedback-dialog`, `max-width`, `padding` e `--programacao-modal-scale`.
3. Se o modal herdar `programacao-feedback-dialog`, sobrescreva no seletor combinado, por exemplo `.programacao-feedback-dialog.nome-do-modal`.
4. Deixe o header full-bleed: container sem padding, header com `width: 100%`, `margin: 0`, `border-radius: 0` e padding próprio.
5. Organize o corpo em blocos:
   - resumo em cards brancos;
   - formulário principal como card branco com `border-left: 3px solid #f57c20`;
   - ações alinhadas em grid, com botões de altura confortável.
6. Atualize teste focado quando o markup/contrato visual for relevante.
7. Rode teste focado do arquivo afetado e, se houver TypeScript alterado, `tsc --noEmit`.
8. Antes de commitar, revise staged diff para não incluir alterações paralelas.

## Tamanho E Proporção

Para modal operacional grande, evite só aumentar o container. Aumente também a densidade do conteúdo.

Padrão recomendado:

```css
.programacao-feedback-dialog.nome-do-modal {
  --programacao-modal-scale: 1;
  width: min(860px, calc(100vw - 24px));
  max-width: min(860px, calc(100vw - 24px));
  max-height: calc(100vh - 48px);
  padding: 0;
  gap: 0;
  overflow: hidden auto;
  border: 1px solid #dbe5f1;
  border-radius: 22px;
  background: #ffffff;
  box-shadow: 0 18px 46px rgba(16, 40, 73, 0.16);
}
```

Evite:

- Modal enorme com campos pequenos soltos no meio.
- Header azul dentro de padding branco.
- Formulário inteiro dentro de card decorativo sem necessidade.
- `max-width` herdado de `540px` quando o modal precisa ser operacional.
- `scale(0.75)` em modal que já está dimensionado corretamente.

## Estrutura Visual

Use esta composição:

```css
.nome-do-modal__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  width: 100%;
  margin: 0;
  padding: 36px 40px 38px;
  color: #ffffff;
  background: #155bd5;
  border-bottom: 3px solid #f57c20;
  border-radius: 0;
}

.nome-do-modal__eyebrow {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  margin: 0 0 8px;
  padding: 0 10px;
  border-radius: 999px;
  border-left: 3px solid #f57c20;
  background: #ffffff;
  color: #f57c20;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.16em;
}

.nome-do-modal__body {
  padding: 16px 20px 20px;
  background: #f7faff;
}

.nome-do-modal__summary {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.nome-do-modal__summary .programacao-table-cell,
.nome-do-modal__form-card {
  border: 1px solid #dbe5f1;
  border-radius: 14px;
  background: #ffffff;
}

.nome-do-modal__summary .programacao-table-cell {
  min-height: 56px;
  justify-content: center;
  padding: 12px 14px;
}

.nome-do-modal__summary .programacao-table-cell:first-child,
.nome-do-modal__form-card {
  border-left: 3px solid #f57c20;
}

.nome-do-modal__form-card {
  display: grid;
  gap: 16px;
  margin-top: 10px;
  padding: 14px;
}
```

## Campos E Botões

```css
.nome-do-modal .settings-field {
  display: grid;
  gap: 8px;
}

.nome-do-modal .settings-label {
  color: #102849;
  font-size: 13px;
  font-weight: 900;
}

.nome-do-modal .settings-label::before {
  content: "";
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 8px;
  border-radius: 999px;
  background: #f57c20;
}

.nome-do-modal .settings-input {
  height: 38px;
  padding: 0 12px;
  border: 1px solid #d4e1ef;
  border-radius: 12px;
  background: #f6f9fd;
  color: #102849;
  font-size: 13px;
  font-weight: 700;
}

.nome-do-modal .settings-input:focus {
  border-color: rgba(245, 124, 32, 0.8);
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(245, 124, 32, 0.12);
}

.nome-do-modal__actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: 0;
}

.nome-do-modal__actions .admin-btn-secondary,
.nome-do-modal__actions .programacao-confirm-dialog__confirm {
  width: 100%;
  min-width: 0;
  min-height: 44px;
  justify-content: center;
  border-radius: 12px;
  font-size: 13px;
}
```

## Exemplo HTML/React

Exemplo em JSX/HTML para copiar a estrutura. Adapte nomes, labels, callbacks e campos ao modal real.

```tsx
<div className="admin-overlay" role="presentation" onClick={onClose}>
  <section
    className="admin-dialog programacao-feedback-dialog nome-do-modal"
    role="dialog"
    aria-modal="true"
    aria-label="Registrar senha da ocorrência"
    onClick={(event) => event.stopPropagation()}
  >
    <header className="programacao-feedback-dialog__header nome-do-modal__header">
      <div>
        <p className="programacao-map-modal__eyebrow nome-do-modal__eyebrow">
          Tratativa da ocorrência
        </p>
        <h2 className="admin-dialog-title">Entrega fora do horário</h2>
        <p className="muted">1000139439 - Cliente Exemplo - 4316902</p>
      </div>

      <button
        type="button"
        className="sac-export-modal__close"
        aria-label="Fechar modal"
        onClick={onClose}
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.9"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
          className="sac-export-modal__close-icon"
        >
          <path d="M18 6 6 18" />
          <path d="m6 6 12 12" />
        </svg>
      </button>
    </header>

    <div className="nome-do-modal__body">
      <section className="nome-do-modal__summary" aria-label="Resumo">
        <div className="programacao-table-cell">
          <strong className="programacao-table-cell__title">6103120989</strong>
          <span className="programacao-table-cell__meta">Plano</span>
        </div>
        <div className="programacao-table-cell">
          <strong className="programacao-table-cell__title">FABIA OLIVEIRA</strong>
          <span className="programacao-table-cell__meta">Motorista</span>
        </div>
      </section>

      <section className="nome-do-modal__form-card" aria-label="Dados da senha">
        <h3>Senha</h3>

        <div className="nome-do-modal__grid">
          <label className="settings-field">
            <span className="settings-label">Senha</span>
            <input className="settings-input" value={senha} onChange={onSenhaChange} />
          </label>

          <label className="settings-field">
            <span className="settings-label">Motivo</span>
            <select className="settings-input settings-select" value={motivo} onChange={onMotivoChange}>
              <option value="">Selecione o motivo</option>
              <option value="Reentrega">Reentrega</option>
              <option value="Segregar">Segregar</option>
              <option value="Devolução">Devolução</option>
            </select>
          </label>
        </div>

        <div className="nome-do-modal__actions">
          <button type="button" className="admin-btn-secondary" onClick={onClose}>
            Fechar
          </button>
          <button type="button" className="programacao-confirm-dialog__confirm" onClick={onSave}>
            Salvar senha
          </button>
        </div>
      </section>
    </div>
  </section>
</div>
```

## Testes Recomendados

Para mudanças de UI, prefira teste de interação no nível do componente/página:

- abrir modal pelo botão/menu real;
- verificar `role="dialog"` e `aria-label`;
- verificar ausência de elementos removidos;
- verificar classes estruturais importantes (`settings-field`, `programacao-confirm-dialog__confirm`, ausência de wrapper antigo);
- salvar/cancelar e conferir callback/payload.

Exemplo de expectativa:

```ts
const dialog = await screen.findByRole("dialog", { name: /ocorrência/i });
const modal = within(dialog);
const region = modal.getByRole("region", { name: "Dados da senha" });

expect(region.querySelector(".wrapper-antigo")).toBeNull();
expect(modal.getByLabelText("Senha").closest(".settings-field")).toBeTruthy();
expect(
  modal.getByRole("button", { name: "Salvar senha" })
    .classList.contains("programacao-confirm-dialog__confirm"),
).toBe(true);
```
