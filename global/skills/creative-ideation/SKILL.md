---
name: creative-ideation
description: Generate original, high-variance, well-structured ideas for products, features, campaigns, content, names, positioning, offers, workflows, and problem-solving. Use when Codex needs to brainstorm, break creative blocks, expand directions, create distinct alternatives, remix an existing concept, or turn a vague challenge into strong idea options with rationale and next steps.
---

# Creative Ideation

## Overview

Generate ideas with deliberate variety, not generic lists. Convert vague prompts into clear opportunity spaces, explore multiple creative angles, and return options that are distinct, usable, and easy to compare.

Prefer novelty with structure. Push beyond the obvious, but keep outputs anchored to the user's goal, constraints, audience, and implementation reality.

## Workflow

### 1. Frame the creative challenge

Extract or infer:

- the objective
- the audience
- the format of the idea
- the level of ambition
- known constraints
- what "better" means in this context

If the request is underspecified, make pragmatic assumptions and state them briefly. Do not block on perfect information unless the missing detail would change the category of ideas entirely.

When the prompt is messy or vague, rewrite it internally as:

`Create [type of idea] for [audience] that achieves [goal] under [constraints], optimized for [success criteria].`

For stronger framing patterns, read [references/problem-framing.md](references/problem-framing.md).

### 2. Choose an ideation mode

Pick one or combine several:

- `breadth`: produce many directions quickly
- `depth`: expand a smaller set into richer concepts
- `contrast`: create sharply different options
- `remix`: combine familiar ingredients in unfamiliar ways
- `repair`: improve a weak or generic existing idea
- `stretch`: propose bold, unexpected, higher-risk concepts
- `practical`: favor feasible ideas with lower implementation risk

State the mode only when useful to the user.

### 3. Deliberately widen the search space

Avoid staying inside the first reasonable answer. Force variation across at least 3 axes when the task benefits from it:

- audience emotion
- tone
- business model
- interaction model
- channel
- metaphor
- timing
- scale
- medium
- constraint inversion

Use contrast intentionally. If two ideas feel like siblings, push one into a different territory.

For ideation tactics and divergence prompts, read [references/idea-generation-patterns.md](references/idea-generation-patterns.md).

### 4. Produce differentiated options

Default to 5-12 options depending on complexity. Each option should be distinguishable on principle, not just wording.

For each strong option, include:

- a short title
- the core idea in 1-3 sentences
- why it is interesting or strategically useful

When valuable, also include:

- target audience
- emotional hook
- implementation sketch
- monetization or growth angle
- risk or tradeoff

Do not pad the list with weak variants. Fewer strong options are better than many shallow ones.

### 5. Evaluate and refine

When the user needs decision support, score or rank ideas against explicit criteria such as:

- originality
- fit to goal
- feasibility
- speed to test
- brand alignment
- differentiation
- commercial upside

Use lightweight evaluation unless the user asks for a formal matrix. For richer selection logic, read [references/evaluation-and-selection.md](references/evaluation-and-selection.md).

### 6. End with momentum

When appropriate, finish with one of these:

- the top 3 to pursue
- how to combine two promising directions
- the fastest experiment to validate demand
- how to make the chosen concept more distinctive
- what information would unlock a stronger next round

## Output Patterns

Match the shape of the response to the request.

### Quick Burst

Use for fast brainstorming.

Format:

1. short idea title
2. one-sentence explanation
3. optional differentiator

### Curated Set

Use when quality matters more than quantity.

Format each idea as:

- `Name`
- `Concept`
- `Why it works`
- `Risk or watchout`

### Idea Matrix

Use when the user wants breadth with categories. Group options by angle such as:

- low-risk vs bold
- premium vs mass-market
- humorous vs serious
- product vs marketing
- short-term vs long-term

### Build-Ready Concepts

Use when the user is likely to execute immediately. Include:

- concept
- target user
- core mechanism
- MVP shape
- go-to-market hook

If the user asks for a specific format, follow it instead.

## Heuristics

- Prefer specificity over motivational fluff.
- Favor tension, contradiction, and surprise when searching for originality.
- Combine unlike domains when the first-pass ideas are too familiar.
- Use constraints as a creative lever, not only as a limitation.
- Give names that carry a point of view, not placeholder labels.
- Escalate originality gradually if the user seems risk-sensitive.
- When improving existing ideas, preserve the useful core and change the boring part.
- When the domain is crowded, search for a sharper audience, mechanism, or emotional promise.

## Anti-Patterns

Do not:

- return generic brainstorm filler
- produce ten versions of the same idea
- confuse slogans with concepts
- optimize for cleverness while ignoring usefulness
- over-explain simple ideas
- ask unnecessary clarification questions when reasonable assumptions are enough
- present weak ideas with equal confidence

## Domain Adaptation

Adjust the ideation lens to the domain.

- For products and SaaS: focus on unmet needs, workflows, moats, retention loops, and testable MVPs.
- For marketing and content: focus on hook, narrative tension, format fit, distribution leverage, and shareability.
- For naming and branding: focus on memorability, signal, category fit, and emotional resonance.
- For operations or internal processes: focus on bottlenecks, automation leverage, incentives, and simplicity.
- For business models and offers: focus on packaging, risk reversal, pricing logic, and differentiation.

## Handling Weak Input

If the user asks only "give me ideas" with little context:

1. infer a likely target based on the surrounding conversation
2. generate a mixed set with clearly different angles
3. label the assumptions briefly
4. invite narrowing only after providing useful options

If the request is blocked by a crucial ambiguity, ask one concise question. Otherwise, move forward.

## References

Read references only when they materially improve the response:

- [references/problem-framing.md](references/problem-framing.md): use when the prompt is vague, overloaded, or strategically unclear
- [references/idea-generation-patterns.md](references/idea-generation-patterns.md): use when you need stronger divergence and more creative range
- [references/evaluation-and-selection.md](references/evaluation-and-selection.md): use when the user wants comparison, ranking, or portfolio selection
- [references/output-recipes.md](references/output-recipes.md): use when you need a tailored response structure for the idea type
## Mandatory Automated Testing Policy
- Automated testing is mandatory for every behavior-changing code change.
- Follow `../_shared/tdd-decente.md` as the quality bar.
- If the ideation output turns into React/UI implementation work with layout toggles or imperative DOM enhancers, preserve the transition-regression rule from `../_shared/tdd-decente.md`.
- If ideation is followed by implementation, require tests that can catch the real user-facing regression, not just helper assertions.

## Automated Test Selection
- Run the automated tests and validations that directly match the changed area and risk.
- Prefer native project commands such as `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint`, or `npm run build` when they are the clearest coverage for the task.
- Do not require the project Python automation runner for routine implementation or review work.
- Use the central automation runner only when the user explicitly asks for it or when a deploy/ship script being executed requires it.
- If relevant tests cannot be run, report the exact validation gap instead of substituting the Python runner by default.