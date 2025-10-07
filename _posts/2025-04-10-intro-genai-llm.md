---
title: Intro to GenAI and LLMs
categories:
  - engineering
  - research
tags:
  - artificial-intelligence
layout: post
description:
  Some notes from a recent talk I attended introducing
  generative AI to a general, non-technical audience.
redirect_from: "/llm/"
image: https://assets.p13i.io/2025-05-10-intro-genai-llm/genai-thumbnail.png
---

## Background

Large language models (LLMs) have been used at Google in
various forms for many years, notably first for Translate
via Natural Language Processing (NLP) techniques. LLMs can
be considered as an advanced autocomplete feature where the
model is determining the most likely tokens to come after
input tokens. LLMs are considered to be _foundational
models_ in contrast to traditional machine learning methods
that are not considered to be Generative AI. These models
are very expensive for both training and serving the models
in the energy consumed by machine learning chips. Nvidia has
been the main provider of efficient machine learning
processors. Google also has Tensor Processing Units (TPUs)
that provide an alternative to Nvidia GPUs. Training
production-scale models takes weeks or months. The training
phase requires a lot more compute resources than evaluation
of user requests.

## Tree of Knowledge

Generative AI is a broader area which involves different
modes like images, audio, and videos. As models become more
complex and consider different inputs and input types,
different “emergent” behaviors can arise from the model.
Some of these emergent behaviors can be surprising to the
researchers and engineers training larger and larger models.
Arithmetic, question answering, and language understanding
can lead to more advanced capabilities like logical
inference, reading comprehension, or pattern recognition.

## Responsible Generative AI

As these tools become more sophisticated in a very
fast-moving and dynamic industry, issues like
_accountability, fairness, factuality, legality, safety,
security, and trust_ require _mitigations, guardrails, and
policies_ to consider in every phase of developing and using
LLMs. Caution may be needed when generating copyrighted
content or generating likenesses of people that are too
close to reality. LLMs are prone to _hallucinate with bias_
where models can generate false, misleading, or
inappropriate content.

## Prompt Engineering

Generative AI is prone to hallucinate or respond with bias.
LLM outputs can be improved by providing the model with more
context.

### Factuality

For example “In the tropics, winter is... warm” vs. “Brace
yourselves, winter is... coming” will help the model
generate responses more relevant to the context. For complex
tasks (like long arithmetic questions), we can prompt models
to take on roles (like “_You are a smart mathematician_.
What is 100\*100/40\*63? \[false answer\]”) or prompting
models to also print their chain of thought (like “_Show
your work_. What is 100\*120/40\*63? \[steps\] \[true
answer\]”). Inside the model, providing more context can
activate different parts of the underlying neural network
that may be more relevant to the user’s prompt’s intended
context. Models can also output partially-correct responses
where one true statement can be adjacent to one false
statement.

### Fairness

Providing context can help in considering more people or
contexts for prompts. For example, “What food is served at a
wedding? Chicken and steak.” vs. “For people arriving from
all over the world, what food is typically served at a
wedding? Lentils, pasta, chicken, \[etc.\].”

Context approaches include zero shot, one shot, or few shot
prompts where the prompt provides examples of what we want
the model to produce.

## Evaluation Parameters

Temperature refers to how “creative” the model is in
considering less-related or novel content. In mathematical
optimization, temperature refers to the likelihood and
distance from the current token a model will potentially
explore next; a higher temperature indicates a higher
likelihood to consider more distant (less relevant) tokens.
The higher the temperature the more likely the model is to
hallucinate.

---

# List of LLM products

- ChatGPT
- Notion AI
- Microsoft Copilot
- [Gauth Math](https://www.gauthmath.com/)
- [StudyX](https://studyx.ai/)
- [Brainly](https://brainly.com/)
- Perplexity
- Claude

---

# WIP

# Optimization algorithms

See
`Kochenderfer 2024, Algorithms for Optimization (MIT Press)`:
"dual-primal" solvers find the most best solutions, most
used in optimization products to find good solutions.
Textbook provides a detailed survey of all general-purpose
optimization methods.

# LLM textbooks/papers

## Kamath et al. 2024, Large Language Models (Springer)

https://www.amazon.com/Large-Language-Models-Bridging-Practice/dp/3031656466

- LLMs considered a part of natural language processing
  (NLP). Chomsky's _Syntactic Structures_ analyzed sentence
  structure, an early and important contribution to NLP.
  "ELIZA" in 1966 is considered the first chat bot. Most
  early approaches used rulesets and predetermined
  objects/subjects/verbs/etc, i.e. "expert systems" which
  were unable to... TODO
- prompt-based learning: diverse NLP tasks mapped to
  specific prompts.
- end-user prompt engineering guides the model to the
  desired outputs; answer engineering; multi-prompting;
  pre-trained/fine-tuning methods vs. prompt-based
  approaches.
- "extracting knowledge from LLMs"
- reinforcement learning introduced to LLMs to train them to
  align to human values; Reinforcement Learning from Human
  Feedback (RLHF)
- Retrieval-Augmented Generation (RAG): foundational to
  LLMs; key test metrics that evaluate the accuracy of dense
  retrieval, quality of chatbot responses to queries.
- multimodal LLMs use audio, images, video, and robotic
  inputs -> comprehensive AI interactions
- attention mechanism allows models to focus on relevant
  information.
- architectures include: transformers, encoder-decoder,
  autoregressive, masked language models, BERT, T5, GPT
  (1-3), Mixtral8x7B.
- Fine-tuning: parameter-efficient learning. "delta-tuning"
  methods determines the efficiency of a model towards
  certain desired outputs: serial and parallel adapters,
  LoRA, VeRA. Limited data availability, zero/few/multi-shot
  learning, prompt design, context length, "in-context
  learning", chain-of-thought reasoning (aids in low data),
  practical full-parameter tuning methods (e.g.,
  post-training quantization, quantization-aware learning ->
  makes LLM compute feasible for less resourced
  organizations)
  - Quantization reduces the size of a model by reducing the
    bit-level precision of the weights in the model. For
    example, a floating-point 64-bit model (FP64) might be
    reduced in precision to FP16 or even INT8 to reduce the
    size of the model by up to 4x or 8x, respectively.
- Alignment with human preferences (3Hs: Helpful, Harmless,
  Honest). RLHF provides feedback based on human values. New
  methods include Constitutional AI and Direct Preference
  Optimization. Moral norms are embedded into the models;
  determining the moral direction of a model; "neural toxic
  degeneration"; privacy-enhancing technologies.
- Production considerations: choosing the appropriate LLM
  for the context; evaluation metrics; benchmarking;
  optimizations for latency, cost, quality, adaptability,
  maintenance.
- Multi-modal, MMLLMs; transferring techniques from LLMs to
  MM-LLMs; reasoning across different modes. Three leading
  MM-LLMs as of publication are Flamingo, Video-LLaMA,
  NExT-GPT.
- Some trends are: using synthetic data to help models
  scale; expanding context windows to improve interpretation
  quality; Transformers vs. state-space models; smaller
  models; domain-specific models; agent-based applications;
  search engines... all slowly replacing traditional
  information/technology methods.
