# ERP Jetta Webhook Map

## Backend

- Processo dedicado: `apps/api/src/webhook-main.ts`
- Modulo dedicado: `apps/api/src/webhook.module.ts`
- Controller atual de disponibilidade: `apps/api/src/modules/availability/availability-webhook.controller.ts`
- Service de regras: `apps/api/src/modules/availability/availability.service.ts`
- Token: `apps/api/src/common/security/webhook-token.service.ts`
- Admin token API: `apps/api/src/modules/admin/admin.controller.ts`

## Tela Admin

- Lista de cards: `apps/web/src/app/admin/webhooks/webhook-links.ts`
- Testes dos links: `apps/web/src/app/admin/webhooks/webhook-links.spec.ts`
- Pagina: `apps/web/src/app/admin/webhooks/page.tsx`
- Menu lateral: `apps/web/src/components/admin-shell.tsx`

## Padroes

- Webhooks publicos ficam em `/api/webhooks/...` no dominio.
- A porta dedicada recebe as rotas internas sem o prefixo `/api`.
- O token deve ser enviado por `X-Webhook-Token` ou `Authorization: Bearer`.
- Nao colocar `?token=` em URL.
- Para Connect Channels, payload comum de contato usa `contact.phonenumber` ou `contact["display-phonenumber"]`.
