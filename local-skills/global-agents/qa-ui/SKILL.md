---
name: qa-ui
description: Validate changed components and browser flows, visual layout, accessibility and responsive states using the project's existing UI tools and QA rules.
---

# QA UI

Read project UI/template rules before edits or QA. Reuse existing components, stories, browser harness and accessibility tools. Identify the states changed: initial/loading, success, empty/error, validation and permission denial where relevant. Persist component or end-to-end assertions at the layer that owns the behavior.

Exercise the actual user action with the intended persona, then verify observable UI and persisted effects when applicable. Check keyboard/focus behavior, labels and error recovery for changed interactions. Select supported viewport/theme combinations that expose actual layout risks; inspect screenshots for clipping, scroll, overlap and contrast. A screenshot does not prove interaction, backend behavior or all responsive states; DOM checks alone do not prove visual quality.

For New Move/Jetta projects whose instructions or adapter require `jetta-qa`, load that installed skill and preserve its persona, template, runtime and visual-delegation requirements, including Terra where specified. These model and runtime rules are project-specific; other projects keep their own rules. If the required visual delegate or browser is unavailable, report visual QA BLOCKED and complete independent checks without claiming visual approval.

Keep durable UI tests in native runners and register them through [QA Suite](../qa-suite/SKILL.md). Attach fresh artifact paths, tested states and viewport dimensions. Respect existing runtime sessions and saved automation settings.
