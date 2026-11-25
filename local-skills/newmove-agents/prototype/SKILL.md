---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## New Move: visual prototypes use the template studio

For New Move UI, follow [Templates New Move](../templates-new-move/SKILL.md#protótipos-visuais-no-estúdio) before the generic UI branch below. Show every screen in the requested scope, including secondary dialogs and relevant states, in the existing interactive studio with per-screen options and controls. Do not build a separate switcher or insert prototype variants into operational routes. Logic-only prototypes still use LOGIC.md.

Explore materially different internal compositions, not just modal dimensions or mascot placement. Follow the [internal variation rules](../templates-new-move/SKILL.md#alternativas-de-composição-interna): vary information hierarchy, attachment presentation, KPI placement, cards, actions and semantic SVGs using compatible existing components. The number of useful alternatives depends on the specific surface; the generic default of three and cap of five do not apply to New Move. Keep the same task, data and capabilities across alternatives so the user can compare fairly.

Populate every alternative with realistic, explicitly mocked data from the same fixture set. Include relevant ready/pending/invalid records, meaningful attachments, short and long content, and locally interactive actions; derive KPI values from those fixtures. Do not deliver empty shells or interchangeable placeholder cards. Use the [approved comparison pattern](../../../docs/templates-revisao-interativa-skill.md#padrão-aprovado-para-as-próximas-prévias--02112026), confirmed by the user on 02/11/2026, as the default for future New Move previews. That approval covers the exploration method, not individual variants or product implementation.

This branch overrides the generic rules below about skipping polish/tests, keeping all state in memory, and folding a winner into real code: preserve review drafts, use the studio's visual and interaction checks, and set `prototypeOnly: true` when only prototyping was requested. Visual approval alone does not authorize implementation. Capture the decision and artifacts without automatically committing, pushing or promoting code.

For an explicit or inherited Obsidian Spec Driven workflow, use [the shared Spec Workspace Adapter](../spec-workspace/SKILL.md): keep runnable prototype code at its normal technical location, and save any Markdown verdict or decision note in `Research/` with links to the spec/ticket. Otherwise follow the existing artifact locations below.

## Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a single shareable HTML file (free-play buttons plus tabbed guided walkthroughs) that pushes the state machine through cases that are hard to reason about on paper, and that a non-developer can drive.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

The two branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

## Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious, but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure.
2. **Trivial to run.** A UI prototype starts from one command in the project's task runner: `pnpm <name>`, `python <path>`, `bun <path>`, etc. A logic demo is a single HTML file the user double-clicks. Either way, no thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE, wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Capture it when done.** Fold any validated decision into the real code, then capture the prototype itself as a **primary source**: commit it to a throwaway branch, out of main, and leave a context pointer to that branch on the implementation issue. Capture the answer too (the verdict and the question it settled) in the issue or a commit. The main branch keeps only the validated decision.
