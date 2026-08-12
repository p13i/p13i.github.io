---
title: "Inverted Coding Paradigm for AI-Assisted SWE"
date: "2026-08-11"
categories:
  - writing
  - engineering
layout: post
tags:
  - artificial-intelligence
  - software-engineering
  - sdlc
  - programming
author: Pramod Kotipalli
description:
  AI agents are producing real outcomes for SWEs. It's
  important for software orgs to adjust their working
  patterns to best leverage in-person collaboration time.
  Let agents code towards specs and acceptance criteria
  matrices, while SWEs, PMs, designers, and other roles
  focus their days on creating artifacts, designs, and plans
  that agents can build out overnight.
permalink: /posts/2026/08/invert-coding-sdlc/
redirect_from: "ai-sdlc"
---

Teachers are most valuable helping students work through
problems rather than delivering hours of lecture content in
a one-way monologue. Eric Mazur developed _peer instruction_
at Harvard in the early 1990s by moving information transfer
out of the classroom and information assimilation into the
classroom, which let Mazur leverage valuable classroom time
to coach students instead of lecturing them[^mazur-1997].
Jonathan Bergmann and Aaron Sams brought the same inversion
to high school chemistry in 2007: while recording lectures
for absent students, they found that the students who
attended used the recordings to review[^bergmann-sams-2012].
Khan Academy popularized the model at scale via the
internet[^khan-2011].

A similar inversion is available for software engineers and
their organizations. Programming may no longer need to
compete with other job functions of a software engineer when
it comes to valuable in-person office time. Specifically,
programming can pivot to an asynchronous or overnight model,
while business hours can focus on code review,
cross-functional collaboration, and workshopping software
plans with agents and humans in the loop.

## Gates are Fewer, More Critical

To analyze what exactly AIs have automated for SWEs, and how
we can reshape the working day, let's trace what a task
requires from end to end:

Assuming a SWE arrives with an appropriate scope of work in
mind:

1. Write up a design doc.
2. Approve the design doc with team feedback.
3. Implement the design doc into code.
4. Iteratively test, validate, and improve code.
5. Send code for review to team.
6. Deploy code.
7. Validate design doc against deployment.

Here, steps 3 and 4 can take up the majority of an
individual contributors time. As I will discuss later,
leveraging loops and test-driven development with agents,
can relocate the implementation and iterative code
improvement work to outside of a human SWE's business hours.

With agents maximally in the loop, we can annotate the
typical SWE workflow from before:

1. Write up a design doc.
   - _Now, with an agent in the loop._
2. Approve the design doc with team feedback.
   - _Cross-functional (XFN) collaborators can embed
     requirements, like UI designs, directly into the design
     doc so agents can build to them._
   - _SWEs write lower-level plans, disambiguating
     implementation choices via interview sessions with
     agents, and develop full test matrices._
3. Implement the design doc into code.
   - _Agents implement code async._
4. Iteratively test, validate, and improve code.
   - _Agents "work backwards" against the comprehensive test
     matrices._
5. Send code for review to team.
   - _Agents pre-review much of the work and fix issues. SWE
     only needs cursory review before sending to team._
6. Deploy code.
   - _Within careful bounds, agents can also debug and
     resolve deployment issues._
7. Validate design doc against deployment.
   - _With full test matrices, agents can pre-verify the
     design doc against prod deployments._

A seven-stage model of SWE can be simplified to four
discrete review gates, requiring the most critical thinking
from the operator:

1. SWEs and cross-functional (XFN) collaborators align on
   requirements in mostly-human written design docs, rich
   with artifacts.
2. SWE developed mostly-prose plan files generated from
   human-authored design docs, ready to hand off to agents.
3. SWEs code review of the agent's output against the plans.
4. SWEs and XFN collaborators manual validate the design doc
   against a deployed system.

Effectively, we should restructure the SWE workday against
these four types of gates, letting programming work become
transparent for SWEs.

Goals and test matrices, in particular, enable this shift of
what business hours entail.

## Specs & Agent Loops

Recent AI systems provide `/goal` features that allow for
"loop engineering" techniques[^orosz-2026]. The result is
that SWEs _no longer have to monitor agents as they write
code_; SWEs can work at the level of plans that specify
detailed test cases.

Agents thrash, _a lot_: they "re-discover" how to use custom
knobs within a system, they work down a train of thought
that leads no where, and so on... the examples are endless,
before we even consider the effects of AI hallucination in
elongating agent SWE timelines.

The key migration for thrash is investing in the matrix of
test cases beforehand so agents can write and work against
comprehensive test suites.

Agents can effectively "work backwards" from failing tests
to find real and correct solutions in almost all domains of
testing, including unit tests, load tests, UI tests, and
service-level objective (SLO) verification. As in
test-driven development, everything that can be encoded via
tests or clear verbal acceptance criteria is a surface of
engineering that SWEs most likely can trust agents to solve
autonomously at human quality.

This test matrix is what makes the async agent shift work.
With agent goal loops, thrash costs wall-clock but async
wall-clock time is abundant, whether overnight, over the
weekends, or during a full day of meetings.

## Collaboration

SWEs' time in the office is best used writing detailed
specs, not writing code or even watching agents write code.
These specs include the full product definition from
end-to-end, incorporating the designs and insights of
cross-functional (XFN) collaborators such as UI designers
and product managers. As the docs are changed during the
day, agents reconcile major new features or changes async so
that the team can come back to the next iteration of work
that was built out for them.

Overall, this pattern lets SWEs work at a more creative
level. Given the capabilities of agents today, spec files
can be detailed documents approachable by many different XFN
roles and still include deep technical details where needed.

## Takeaways

The fast-advancing capabilities of AI systems have already
shown us that specific job functions like programming can be
highly automated. The time that frees up gets reallocated to
async and off-hours work, much like the inverted classroom
model from Khan Academy.

To leverage agents' ability to deliver real,
production-level code and to maximize the utility of
in-person collaboration, it's important for both ICs and
orgs to start inverting code-based workstreams: let the code
get written overnight, and spend the day at the gates, the
specs, and the people.

## References

[^mazur-1997]:
    [Eric Mazur, _Peer Instruction: A User's Manual_, Prentice Hall, 1997](https://mazur.harvard.edu/publications/peer-instruction-users-manual)

[^bergmann-sams-2012]:
    [Jonathan Bergmann and Aaron Sams, _Flip Your Classroom: Reach Every Student in Every Class Every Day_, ISTE/ASCD, 2012](https://www.ascd.org/books/flip-your-classroom)

[^khan-2011]:
    [Sal Khan, "Let's use video to reinvent education", TED2011, March 2011](https://www.ted.com/talks/sal_khan_let_s_use_video_to_reinvent_education)

[^orosz-2026]:
    [Gergely Orosz, "What is 'loop engineering?'", The Pragmatic Engineer, July 14, 2026](https://newsletter.pragmaticengineer.com/p/what-is-loop-engineering)
