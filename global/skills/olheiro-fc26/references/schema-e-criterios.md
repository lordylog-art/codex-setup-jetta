# Schema e critérios do Olheiro FC 26

## Campos principais

- `playerid`, `name`, `age`, `birthdate_gregorian_days`
- `club.teamid`, `club.name`; `club = null` indica vínculo não encontrado
- `ratings.overall`, `ratings.potential`, `ratings.international_reputation`
- `positions.primary.name`, `positions.alternatives[].name`
- `stars.skill_moves`, `stars.weak_foot`
- `physical.height_cm`, `weight_kg`, `preferred_foot_code`
- `attributes.*`
- `roles.role1..role5`
- `playstyles.regular[]`, `playstyles.plus[]`, `hidden_career_traits[]`
- `financials.market_value`, `release_clause`, `wage`
- `contract.raw_fields`, `squad_links[]`, `raw_fields`

Campo ausente ou `null` significa indisponível, não zero.

## Posições

`GK, SW, RWB, RB, RCB, CB, LCB, LB, LWB, RDM, CDM, LDM, RM, RCM, CM, LCM, LM, RAM, CAM, LAM, RF, CF, LF, RW, RS, ST, LS, LW`.

## PlayStyles de linha

Finesse Shot, Chip Shot, Power Shot, Dead Ball, Precision Header, Acrobatic, Low Driven Shot, Gamechanger, Incisive Pass, Pinged Pass, Long Ball Pass, Tiki Taka, Whipped Pass, Inventive, Jockey, Block, Intercept, Anticipate, Slide Tackle, Aerial Fortress, Technical, Rapid, First Touch, Trickster, Press Proven, Quick Step, Relentless, Long Throw, Bruiser, Enforcer.

## PlayStyles de goleiro

GK Far Throw, GK Footwork, GK Cross Claimer, GK Rush Out, GK Far Reach, GK Deflector.

## Atributos exportados

Goleiro: `gkdiving`, `gkhandling`, `gkkicking`, `gkpositioning`, `gkreflexes`.

Linha: `crossing`, `finishing`, `headingaccuracy`, `shortpassing`, `volleys`, `defensiveawareness`, `standingtackle`, `slidingtackle`, `dribbling`, `curve`, `freekickaccuracy`, `longpassing`, `ballcontrol`, `shotpower`, `jumping`, `stamina`, `strength`, `longshots`, `acceleration`, `sprintspeed`, `agility`, `reactions`, `balance`, `aggression`, `composure`, `interceptions`, `positioning`, `vision`, `penalties`.

## Heurísticas funcionais

- Finalizador: finishing, positioning, composure, shotpower; Finesse/Power/Low Driven.
- Ponta: acceleration, sprintspeed, dribbling, agility; Rapid/Quick Step/Technical.
- Criador: vision, shortpassing, longpassing, curve; Incisive Pass/Tiki Taka/Inventive.
- Volante: interceptions, defensiveawareness, stamina, strength; Intercept/Anticipate/Relentless.
- Zagueiro: defensiveawareness, standingtackle, strength, heading; Anticipate/Block/Aerial Fortress.
- Lateral: pace, stamina, crossing, tackling; Whipped Pass/Relentless/Jockey.
- Goleiro: usar somente atributos e PlayStyles de goleiro como evidência principal.

## Financeiro

Valores financeiros são brutos do save e sua moeda/unidade deve ser tratada como a exibida no jogo. O ranker usa market value e, na ausência, release clause para comparar com orçamento. Ausência permanece `unknown`; não estimar automaticamente.
