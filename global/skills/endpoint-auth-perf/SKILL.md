---
name: endpoint-auth-perf
description: Validar e otimizar endpoints autenticados na prática: fazer login real antes da chamada, evitar 401 falso, medir tempo/status/body do endpoint, comparar antes/depois, investigar gargalos e repetir até ter evidência objetiva. Use quando o usuário pedir para testar endpoint direto, medir performance de API autenticada, reproduzir lentidão de tela via API, chamar endpoint depois do login, ou otimizar backend com prova real.
---

# Endpoint Auth Perf

## Objetivo

Provar o comportamento e o tempo real de um endpoint autenticado com o menor fluxo confiável:
login real, cookie/token real, chamada direta ao endpoint, medição, correção mínima e nova medição.

## Quando Usar

- Endpoint retorna `401` quando testado sem sessão.
- Tela está lenta e é preciso separar custo de backend, web proxy e render.
- O usuário pede para testar rota/API “logado”.
- Uma otimização precisa de evidência antes/depois.
- Busca, paginação, filtros ou carregamento inicial parecem lentos.

## Fluxo

1. Identifique o alvo real:
   - URL do endpoint.
   - método HTTP.
   - query/body exatos.
   - ambiente local, staging ou produção, preferindo local/staging.

2. Descubra o login existente no projeto:
   - procure scripts, testes e rotas de auth já usados;
   - não invente payload de login;
   - use variáveis locais como `TEST_LOGIN_EMAIL` e `TEST_LOGIN_PASSWORD` quando já existirem;
   - nunca imprima senha, token, cookie completo ou segredo.

3. Verifique servidores e portas:
   - confira se API/web estão ouvindo;
   - se precisar subir dev server, use processo oculto/background e registre logs;
   - aguarde health ou resposta HTTP antes de medir.

4. Faça uma chamada negativa rápida quando fizer sentido:
   - sem cookie/token deve retornar `401`/`403`;
   - isso prova que o teste autenticado não está burlando segurança.

5. Faça login e capture credencial:
   - cookie `Set-Cookie`, bearer token ou mecanismo real do projeto;
   - reporte só `hasCookie: true` ou equivalente.

6. Meça o endpoint:
   - tempo total em ms;
   - status HTTP;
   - tamanho/quantidade relevante (`itemCount`, `total`, primeiro item sanitizado);
   - erro resumido se falhar.

7. Se estiver lento:
   - isole se a lentidão está no web proxy, API interna, banco ou render;
   - teste endpoint web e endpoint interno quando existirem;
   - prefira medir a mesma query antes/depois.

8. Corrija cirurgicamente:
   - mova trabalho caro para depois de paginação quando seguro;
   - filtre antes de hidratar dados pesados;
   - evite joins/subqueries por linha em universo grande;
   - mantenha contratos existentes;
   - não crie tabela/cache novo sem pedido explícito.

9. Repita a medição:
   - mesma chamada;
   - mesmo ambiente;
   - reporte antes/depois com números absolutos.

## Evidência Mínima

Ao finalizar, informe:

- login realizado: status e se capturou cookie/token, sem revelar o valor;
- endpoint testado;
- status HTTP;
- tempo em ms;
- quantidade de itens/resultado encontrado;
- comparação antes/depois quando houver;
- testes automatizados rodados;
- o que não foi validado.

## Segurança

- Não imprimir secrets, cookies, tokens, senhas ou `.env`.
- Não usar produção para chamadas com efeito colateral sem autorização explícita.
- Para `GET`, ainda considerar dados sensíveis no body/log.
- Para `POST/PATCH/DELETE`, preferir ambiente local/staging ou payload descartável.

## Exemplo de Medição

Use Node/PowerShell ou ferramenta nativa do projeto. O formato abaixo é o padrão desejado de saída sanitizada:

```json
{"label":"login","status":201,"hasCookie":true}
{"label":"endpoint-alvo","status":200,"ms":863,"itemCount":2,"first":{"id":"...","status":"..."}}
```

## Heurísticas de Performance

- Se busca específica é rápida e listagem aberta é lenta, o problema costuma estar antes da paginação.
- Se endpoint web é lento e API interna é rápida, investigar proxy/transformação no Next.
- Se API interna é lenta, investigar SQL, índices, joins laterais, CTEs, hidratação e N+1.
- Se primeira chamada é lenta e segunda é rápida, separar cache, cold start e execução real.
- Se retorna poucos itens após muito tempo, procure trabalho feito em massa antes do `LIMIT`.
