---
title: "Course Notes: Intro to HCI & Design Thinking 
(Stanford CS 147)"
categories:
- writing
tags:
- human-computer-interaction
layout: post
description: "CS 147 is a course on Human-Computer 
Interaction (HCI) and Design Thinking offered at Stanford 
University taught by Professor James Landay. These notes 
were prepared for the Winter 2022 course delivered in a 
hybrid format due to COVID-19. The course introduces 
principles for designing and evaluating user interfaces."
---

# Introduction

The academic field of human-computer interaction (HCI) has 
grown considerably in the past two decades as mobile and
desktop technologies are now used by and impact billions of
people all around the world.

This course synthesizes key research findings, provides
practical approaches to user interface (UI) prototyping, and
a strong introduction to the *design thinking* process
developed by the Hasso-Plattner Institute and Stanford
University to create experiences that are grounded in
observations of how real people use software products.

These course notes are summaries of key points in
pre-lecture reading materials and lectures including key
graphics and resources to better illustrate and aid in 
learning.

**Note from the author:** Please do note that these are *my*
(Pramod's) own notes and may not fully reflect the learning
outcomes of James Landay's course; howerver, I will do the
best I can to write an introduction to HCI faithful to the
teachings of James Landay and his wonderful staff of course
assistants.

## Course overview

The PDF screen-grab of the syllabus for this course is 
available here: 

{% include _single_download.html 
    name="🗓 CS 147 (Winter 2022) Calendar (3.1 MB)" 
    url="https://github.com/p13i/p13i.github.io/files/9128690/cs147-2022-wi-calendar.pdf"%}

These course notes will consist of `10` major sections based
on the organization of the two hour lecture periods over the
ten week Stanford quarter.

1. 1A: Introduction to HCI and a Techno-Realist Vision
2. Design Thinking:
    1. Design Discovery (1B)
    2. Define (2A)
    3. Ideate (2B)
    4. Concept Videos (3B)
    5. Exploration (4A)
    6. Early Stage Prototyping (4B)
3. Visual Information Design (5B)
4. Early and Future Visions of HCI (6A)
5. Human Abilities (6B)
6. Heuristic Evaluation (7A)
7. Conceptual Models and Interface Metaphors (7B)
8. Usability Testing (9A)
9. Design Patterns (9B)
10. Smart Interfaces for Human-Centered AI (10B)

Let's get into it!

# Lecture 1A: Introduction to HCI and a Techno-Realist Vision

## Pre-Lecture Readings

### [Stewart 2021] *From techno-optimism to techno-realism: What it means to innovate responsibly*

{% include _single_download.html 
    name="📜 PDF from Medium.com (363 KB)" 
    url="https://github.com/p13i/p13i.github.io/files/9128997/Stewart.2021.From.techno-optimism.to.techno-realism.-.what.it.means.to.innovate.responsibly.pdf"%}

Stewart discusses how to innovate responsibly when building
for a diverse and global community, as Facebook does.
Unbridled technology-optimism isn’t a healthy approach to
responsible innovation, i.e. the belief that technology
advancements are always a net positive contribution to our
world. 

By leveraging a diverse set of perspectives, technology can
empower people and should be developed collaboratively with
the intended users. The technologies we deploy may
unintentionally reinforce or amplify the pre-existing
prejudices. 

In designing new virtual assistant voices, Stewart’s
Responsible Innovation team reflected early in the design
process to challenge the status quo that a voice assistant
should have a female persona and voice. This is a
socially-aware lens applied to development. 

Beyond the “target users” of a product, we should also
consider who would be impacted by others’ use of the product
via an **expansive stakeholder analysis**. This process is
augmented by **codesign** wherein community members are
treated as equal collaborators in the design process via a
participatory approach. Participants were paid a “meaningful
honorarium” for their engagement. 

To empower people, reduce reinforcing existing societal
biases, and improve the condition of others, technologies
need to expand their scope of professional responsibility,
as a *digital urban planner* of sorts.

## Lecture on 2022-01-03

### AI & User experience design

Tesla’s autopilot feature requires UX design. The
touchscreen requires your full attention to operate it, a
mode ripe for multi-modal interactions involving more than
one interaction mode (e.g., voice with a screen output,
gestures to a voice output).

![Tesla Autopilot](https://user-images.githubusercontent.com/13140065/180309680-ac8c1250-c611-4c16-9f0e-e31c61ae37c4.jpg)

(Image: [Roberto Nickson, Unsplash](https://unsplash.com/photos/Ddjl0Cicdr4))

Smart speakers use a voice UI but do not provide a natural
interaction with context and knowledge about the user. In
general, what should we show to a user? Who are other
stakeholders and what should they see from an AI system. Are
there design patterns to support smart UIs?

### Balancing design thinking & technology

A balance between human-centered approaches and technical
approaches in CS/engineering. Design involves:

1. **Humans**: the end users, cognition, vision, perception,
motor abilities, etc. 
2. **Tasks & Activities** we want to support for the people
we are designing for 
3. **Technology**: what users already have or new tech we
might bring to them. This synthesis takes context in
organizational and societal issues.

### Design discovery and exploring ideas 

The **Design Thinking** process is outlined to the right.
Beyond a seemingly-linear process, there are loops or steps
back in this process. 

![Five stage design thinking process](https://user-images.githubusercontent.com/13140065/198849919-f4e708f5-cdd1-4ae1-aa84-c2fd17f1da9f.png)

User experience goals include: 

1. Learnable: faster the second time 
2. Memorable: from session to session 
3. Flexible: multiple ways to do tasks
4. Efficient: perform tasks quickly 
5. Robust: minimal error rates, good feedback so user can
recover
6. Discoverable: learn new features over time 
7. Pleasing: high user satisfaction 
8. Fun

User-centered design involves:
1. Cognitive abilities: perception, physical manipulation,
memory
2. Organizational/education job abilities 
3. Keeping users involved throughout: developers working
with target customers, think of the world in the users’
terms 

Accessible design involves catering to:
1. Different abilities: vision, hearing, cognitive, mobility
(e.g., blind users with screen readers)
2. Moral and ethical purpose: inclusive design benefits
everyone (e.g., sidewalk curb cuts)
3. Legal guidance: Americans with Disabilities Act (ADA)
which includes websites and apps per the Department of
Justice

Needfinding involves observing existing practices for
inspiration making sure that key questions are answered
including ethical questions in design with underserved
communities. Needfinding transforms into sketching and
storyboarding. Concept videos illustrate the context of the
user rather than the specific UI, a relatively quick and
inexpensive process that forces us to think about how the
user will actually use the app.

### Rapid prototyping & evaluation 

Rapid prototypes allow us to build a mock-up of a design so
it can be tested, typically taking the form of paper
sketches or interactive tools like HTML, Balsamiq, Axure,
proto.io, Sketch, Marvel, Modao, etc. UI builders include
Expression Blend with Visual Studio, Xcode’s Interface
Builder, etc. Test with real customers (“participants”) with
an interactive prototype. Low-cost techniques involve expert
evaluation (heuristic evaluation).

# Design Discovery

## Pre-Lecture Readings

### Adams 2013, 4 Steps to Successful Brainstorming

{% include _single_download.html 
    name="📜 PDF from Medium.com (355 KB)" 
    url="https://github.com/p13i/p13i.github.io/files/9894489/Adams.2013.4.Steps.to.Successful.Brainstorming.pdf"%}

Adams found that most corporate executives put the cart
before the horse: “Instead of parsing the objectives they
hope to achieve, they direct their energy at coming up with
solutions to broadly-stated problems.” Keeney argues that
before brainstorming, it is important to analyze and focus
on the objectives of the group. Keeney’s four steps to
effective brainstorming are:

1. Lay out the problem you want to solve. Identify the
objectives, evaluate the alternatives (pushing until five
such alternatives are found), and select the best option.
2. Identify the objectives of a possible solution. Going
into details about the requirements and not potential
solutions makes the forthcoming brainstorming sessions more
successful.
3. Try to generate solutions individually. Before heading to
the group, brainstorm solutions individually to avoid
‘anchoring’ to a particular solution/objective to the
exclusion of other goals for the team.
4. After the prior steps, work as a group. Use the
objectives, problem statements, and individual solutions to
facilitate a more productive brainstorming session.

### Beyer, *Contextual Design - Defining Customer-Centered Systems*

{% include _single_download.html 
    name="📜 PDF on my Google Drive" 
    url="https://drive.google.com/open?id=1bif2O_v-Q2MoPpNenZ7zosDeh52LLGE7"%}

Contextual inquiry is all about going to where the customer
(i.e., “user” or “participant”) is, observing them, and
talking to them about their work. A relationship model
suggests that the appropriate behavior will manifest from
the right mindset applied to an interaction with a customer.
Different relationship models bring with them different
attitudes and behaviors taken to the customer. “As long as
you play your role, you will pull the customer into playing
theirs.”

The Master-Apprentice Model is an effective way to collect
data on another. In this case, the design team wants to
learn about the customer’s work from its customers. The
customer (like a master) teaches by doing work and talking
about it while doing the work, making learning easy. We can
have customers explaining their work as they do it, but
customers may not be aware of everything they do or why they
do it. By having the customer talk through their process, we
avoid the “human propensity to talk in generalizations that
omit the detail designers need.” By observing how multiple
such customers work, the design can begin to conceptualize a
system that supports those tasks. Taking notes and asking
about the artifacts in a customer’s environment helps the
designer gain more understanding.

Four principles guide contextual inquiry:

1. **Context** tells us to get as close to being physically
   present in the customer’s environment, allowing us to
   capture concrete data over an ongoing experience (in
   contrast to abstract data from a summary experience).
   Concrete data can be focused on by pulling the customer
   back to the real experience whenever the conversation
   veers off track. Grounding such questions in artifacts
   helps (e.g., “can I see that email you mentioned?”) which
   also serves to stimulate the customer’s memory.. Also,
   ask questions to fill in gaps in understanding.

2. **Partnership** is about making the customer and design
   feel like they are collaborating in understanding the
   customer’s work. In this process, the designer alternates
   between watching a customer and probing into their
   behaviors and environment. Such probes can also guide the
   customer to provide details themselves as the interview
   experience continues. Assumptions or potential design
   solutions can be proposed to the customer to clarify
   assumptions. Be a “partner in inquiry.”

3. **Interpretation** is the “chain of reasoning that turns
   a fat into an action relevant to the designer’s intent.”
   Interpretation drives design decisions. The
   interpretation is grounded in facts, moves to a
   hypothesis which has an implication realized as a design
   idea. The apprentice can clarify their understanding of a
   task or structure by asking the customer directly to
   clarify. This approach helps the designer mitigate their
   own assumptions.

4. **Focus** helps keep the conversation focused on what
   work is relevant to the design without fully taking
   control from the customer. If the designer thinks some
   behavior is happening for no reason, then the designer
   doesn’t yet understand the point of view from which that
   behavior does make sense. Admit your ignorance, and
   always assume there is more to be learned.

> If you think it’s for no reason, you don’t yet understand
> the point of view from which it makes sense. [Beyer,
> Contextual Design, p. 63]

Beyer outlines a structure for contextual interviews that
Landay discusses in detail in lecture.
