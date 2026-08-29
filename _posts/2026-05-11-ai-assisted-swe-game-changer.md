---
title: "AI-Assisted SWE Game Changer"
date: "2026-05-11"
categories:
  - engineering
  - writing
tags:
  - agents
  - software-engineering
  - artificial-intelligence
  - m2
  - mycool-games
layout: post
author: Pramod Kotipalli
description:
  A WIP account of using the M2 manager-of-managers protocol
  to build the complex 3d.mycool.games editor through
  durable, provable, long-running AI-assisted SWE.
---

What changes when an AI system can keep building software
for eight hours from one prompt?

This is the practical question I have been exploring with
M2. I do not mean "can an AI write code?" That question is
already too small. A model can write a useful function, a
test, a refactor, or a small feature. It can also fail in
all the familiar ways: it can lose context, forget why a
decision was made, stop after opening a pull request, wait
for CI as if waiting were progress, or leave behind a
summary that sounds plausible but cannot actually resume the
work.

The more interesting question is whether AI-assisted
software engineering can become durable. In other words, can
an AI system keep track of a complex product goal, split the
work into lanes, dispatch workers, review results, collect
evidence, update pull requests, and then resume later from a
real state record rather than from vibes?

For me, this is where M2 has started to feel like a game
changer.

M2 means "manager of managers." It does not mean milestone
2. It is a protocol I have been using in my `cs` monorepo to
turn one prompt into a long-running control plane for
software work. The best current example is
`3d.mycool.games`, a complex browser-based 3D editor studio
with Cinema 4D-style interaction goals, an SDL/WASM canvas,
viewport controls, object and component editing, material
UX, snapping, PBRT export, render proof, and a growing body
of validation artifacts.

This post is a WIP account of that system. Some of the work
is still rough. The public explanation is behind the private
implementation. The protocol has some sharp edges. However,
the core idea has become concrete enough that I want to
write it down: AI-assisted SWE changes character when the
unit of interaction is not a single completion, but a
durable engineering run.

## Background

Most AI coding workflows still feel like a conversation with
a very fast individual contributor. That is useful. I use
that mode constantly. It helps with local reasoning,
boilerplate, tests, migrations, and understanding unfamiliar
code.

However, a serious software project is not only a sequence
of code edits. It is also product judgment, review,
validation, handoff, integration, rollback, and remembering
which constraints matter. The work is social even when only
one human is involved, because the project needs different
roles at different times.

For example, a 3D editor needs a product view of what the
user is trying to do. It needs runtime data structures for
scene objects, components, command history, and
serialization. It needs UI judgment about how a viewport
should feel. It needs renderer and picking logic. It needs
tests and browser proof. It needs delivery discipline so the
branch does not become an enormous, unreviewable pile.

When I tried to push that kind of project through ordinary
single-agent prompting, the weak point was not that the
model could not write code. The weak point was continuity.
What happened two hours ago? Which gate was actually red?
Which branch was the active one? Did the screenshot prove
the exact commit, or just some previous local state? Did the
PR represent the end of the work, or just a checkpoint?

Those questions sound mundane, but they are exactly where
long-running software work lives.

## What M2 Is

M2 is my attempt to make that long-running work explicit.
The protocol coordinates a top-level conductor, subteam
managers, implementation workers, testers, reviewers,
verification workers, and delivery workers. In ordinary
language, it is a way to ask one AI system to behave less
like a lone coder and more like a small engineering org with
memory.

The invocation is intentionally small. For the 3D editor
project, the shape is:

```text
m2(.agents/projects/2026-04-21-3d-mycool-games-cinema-4d-pbrt-m2/plan.m2.gpt.md,
iterations:8192, duration:8h, numM1s:4)
```

The important part is not the syntax. The important part is
what the syntax points to. The `.plan.m2.gpt.md` file is not
just a TODO list. It is an orchestration entrypoint. It
declares the product intent, the project file network, the
manager graph, the work packets, the review and
verification rules, the durable state requirements, and the
acceptance rows that define whether the project is actually
moving.

By "M1" I mean a manager lane underneath the M2 conductor.
In the 3D project, I have used multiple M1 lanes at once.
One lane may focus on spatial editor depth. Another may work
on UI breadth. Another may harden PBRT output behavior. A
fourth may collect evidence and delivery proof. M2 is
responsible for keeping those lanes coherent instead of
turning them into four unrelated coding sessions.

This distinction matters. Without a control plane, parallel
agents are just parallel risk. With a control plane, they
can become parallel engineering work.

## The 3D Editor Problem

`3d.mycool.games` began as a much simpler 3D surface. The
current goal is more ambitious: a browser-accessible model
editor that feels closer to a real DCC tool than to a toy
canvas demo. DCC means digital content creation. These are
tools like Cinema 4D, Blender, Maya, and other systems where
the user thinks spatially, edits objects directly, and
expects the viewport to preserve a lot of subtle state.

That kind of editor is hard because the important behavior
is not isolated in one function. It crosses many layers:

- Input has to distinguish orbit, pan, zoom, selection,
  dragging, cancellation, and command shortcuts.
- The runtime has to represent objects, components,
  transforms, materials, visibility, locking, and undo
  state.
- The viewport has to give spatial feedback: axes, snap
  labels, confidence readouts, hover and selected states,
  and camera memory.
- The browser/WASM build has to prove that the canvas is
  nonblank, framed correctly, and free of obvious console or
  page errors.
- The PBRT path has to export scenes, handle inactive or
  failing render workers, and return structured diagnostic
  information.

The acceptance matrix for the project reflects this
complexity. It does not only say "make editor better." It
names concrete gates such as navigation bindings,
orbit/pan/zoom, frame memory, selection confidence,
axis/plane snapping, point/edge/face component modes,
cancel/undo/redo, and localhost demo freshness.

This is where I started to need more than an assistant. I
needed an operating rhythm.

## One Prompt, Many Lanes

The surprising thing about the M2 runs is how much work can
be hidden behind a small prompt, while still remaining
auditable.

The human prompt says, in effect, "run the 3D project." M2
then loads the plan, project manifest, packet registry,
acceptance matrix, file leases, manager files, and resume
state. The conductor does not need me to manually tell one
agent to inspect the runtime, another to check browser
evidence, another to update the PR, and another to write the
handoff. Those responsibilities are part of the protocol and
project network.

For the 3D editor, the manager graph includes product,
runtime, editor UX, preview, PBRT bridge, verification, and
delivery. That split is useful because each role cares about
a different failure mode.

The product manager cares whether a user can actually
create, navigate, select, edit, render, and recover. The
runtime manager cares whether the scene graph and command
model are coherent. The editor UX manager cares whether the
controls feel spatially understandable. The preview manager
cares about camera projection, object IDs, highlighting, and
performance. The PBRT bridge manager cares about export and
render contracts. Verification cares about proof. Delivery
cares about branch hygiene, PR shape, and resumability.

In other words, M2 lets the prompt name the goal while the
project files preserve the division of responsibility.

That has allowed long-running operations of eight or more
hours to move real product surface area without me manually
orchestrating each agent. The orchestration still exists.
It is just encoded in the M2 protocol and the project
artifacts rather than living in my head or in a fragile chat
thread.

## Durable Means Resumable

By durable, I mean that the run leaves behind enough state
for the work to resume without relying on the last few
messages of chat history.

M2 writes and refreshes artifacts such as:

- a run event log;
- a board of packet state;
- a resume cockpit for the human;
- a runnable resume prompt for the next invocation;
- a project-level pointer to the latest compatible resume
  prompt;
- acceptance and evidence records;
- PR and branch checkpoints.

This sounds bureaucratic, but it has a practical purpose.
Long-running AI work fails if the only durable record is a
paragraph that says "I made progress on the editor." That is
not a handoff. A usable handoff needs to say what branch is
active, what commit was proven, what URL was tested, what
packets moved, what remains blocked, what evidence is fresh,
and what exact invocation should continue the run.

For example, a resume capsule for the 3D project can point
to an implementation worktree, a branch, a pull request, a
localhost proof URL, a latest product commit, the current
demo URL, the active lane plan, and the minimum wall-clock
policy for the next run. A bare `m2(...)` invocation can
then hydrate that saved prompt and continue as if I had
pasted the full state back into the session.

This is one of the most important differences from ordinary
AI coding. The memory is not mystical. It is a file.

## Provable Means Evidence-Driven

By provable, I do not mean formally verified. I mean that a
claim about progress should be tied to evidence.

In the 3D editor project, a completed packet is not supposed
to be completed by narration. Verification records the exact
command, working directory, commit SHA, worktree path, exit
code, timestamp, browser route, viewport, screenshot path,
canvas pixel proof, render artifact proof, and next action
for blocked rows.

This matters because UI work is easy to fool yourself about.
An agent can say the editor works. A screenshot can prove the
canvas is nonblank. A browser report can prove there were no
console errors. A pixel check can prove the WebAssembly
surface rendered something at the expected dimensions. A
commit SHA can prove the screenshot came from the exact code
being discussed.

The 3D runs use exact-head localhost proof and PR proof as
part of the delivery rhythm. The pattern is:

1. choose a packet or small visible behavior slice;
2. edit in the active implementation worktree;
3. run the smallest relevant local checks;
4. refresh the localhost demo from that exact head;
5. capture browser or screenshot proof;
6. push a coherent commit or PR update;
7. record the evidence and resume state;
8. continue while safe work remains.

That last step is easy to miss. In M2, opening a PR is not
the finish line. It is a delivery checkpoint. Pending CI is
not a reason to stop if other safe packets can move. A
ready-for-review branch is useful, but it is not the same as
terminal product state.

This is a small cultural shift. It pushes the agent away
from "I did a thing" and toward "the system moved from this
state to that state, and here is the proof."

## What It Has Been Building

The recent 3D runs have moved across several streams at the
same time.

On the spatial editor side, the project has been adding
direct manipulation readouts, component drag resolution,
axis labels, snap tiers, local and world deltas, confidence
metadata, and object/component selection surfaces. These are
the kinds of features that make a viewport feel less like a
flat canvas and more like an editor with a spatial model of
the user's intent.

On the SDL UI side, the project has been adding
canvas-owned outliner and object action surfaces, keyboard
accelerator readouts, inspector focus telemetry, hierarchy
readouts, and denser status information. This is not glamour
work, but it is important. A 3D editor becomes usable when
the user can see what is selected, what can happen next, and
how the current action maps to the scene.

On the PBRT side, the project has been hardening render
contracts: inactive render responses, byte-suppressed image
responses, oversized request handling, bad UTF-8 handling,
PNG metadata cases, and structured diagnostics when the
bridge or output shape is wrong. This keeps rendering from
being a magic black box.

On the evidence side, the project has been expanding
localhost validation gates. The exact numbers change as the
validator grows, but the important pattern is that each
claim of product progress is accompanied by a fresh proof
bundle from the relevant build.

This is why I think "AI-assisted SWE" undersells what is
happening. The interesting thing is not one model writing
one patch. The interesting thing is sustained engineering
motion across product, implementation, validation, review,
and delivery.

## What Still Needs Work

M2 is not magic, and I do not want to describe it like a
product launch. It is powerful because it is structured, but
that structure also needs care.

The protocol can become too artifact-heavy if every support
file is treated as equally important as product motion. The
project still needs human judgment about priority. Evidence
can go stale. Parallel lanes can collide if file leases are
too vague. A browser proof can prove the wrong thing if the
fixture is weak. A long-running invocation still needs
clear stop conditions so "keep working" does not become
busy motion.

There is also a public explanation problem. The internal
artifacts are useful to the system, but they are not a good
reader experience by themselves. The right public story is
not "look at all these protocol files." The story is that
software agents become more useful when they have durable
state, explicit roles, acceptance gates, evidence, and a way
to resume.

In other words, the protocol is not the product. The
engineering behavior it enables is the product.

## Why This Feels Different

The phrase "AI-assisted SWE game changer" is easy to make
too grand. I am using it in a specific way.

The game changer is not that the model is smarter in one
turn. The game changer is that the work can survive across
turns. It can survive across branches, worktrees, PRs,
browser sessions, test runs, partial failures, and resume
prompts. It can keep moving through an eight-hour run
without requiring me to manually tell every agent what to do
next.

For me, that changes the shape of software work. Instead of
using AI only as a local accelerator, I can start to use it
as an engineering process participant. It can hold a board.
It can ask whether evidence is fresh. It can remember that
the current priority is visible editor behavior, not
infrastructure churn. It can keep one lane on depth and
another on breadth. It can treat a PR as a checkpoint
instead of a stopping point.

That is still early. It is still messy. It still needs a
human owner. However, it points at a different future for
software tools: not just code completion, not just chat, but
durable collaboration with systems that can keep their own
work legible.

That is what I have been trying to build with M2, and that
is what `3d.mycool.games` is helping me test.
