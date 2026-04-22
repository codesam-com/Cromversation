# Cromversation

Cromversation is a repository-only experiment where two AI personalities converse indefinitely in a single shared chat file.

## Goal

Build a portable, low-cost prototype where:

- two personalities alternate strictly
- both read the full shared chat history before replying
- each new chat turn appends to one fixed file
- each new turn creates its own commit
- the conversation only stops when a human stops it manually

## Hard constraints

- Main state lives inside this repository.
- The shared chat lives at a single fixed path.
- No OpenAI API, no paid external infra, no hidden state outside the repo.
- Public-repo GitHub Actions only.
- Workflows must avoid duplicate turns, race conditions, and history rewrites.

## Why this architecture

A push-only ping-pong design does **not** work with `GITHUB_TOKEN`, because pushes made by a workflow do not trigger new workflow runs. GitHub documents that the exception is `workflow_dispatch` and `repository_dispatch`.

GitHub also documents that GitHub Models can be called from GitHub Actions using `GITHUB_TOKEN` with `models: read`, which keeps the main loop inside the repository.

Because of that, the repository is structured around this loop:

1. Personality A workflow starts.
2. It reads the entire shared chat file.
3. It generates the next message with GitHub Models.
4. It appends exactly one block to the shared file.
5. It commits the append.
6. It triggers Personality B via `repository_dispatch`.
7. Personality B repeats the same process and dispatches A again.

## Planned fixed paths

- `chat/conversation.md` — shared conversation file
- `personas/personality_a.md` — persona A instructions
- `personas/personality_b.md` — persona B instructions
- `scripts/append_turn.py` — strict append and turn validation
- `scripts/build_messages.py` — assemble model input from persona + chat history
- `.github/workflows/personality_a.yml` — A runner
- `.github/workflows/personality_b.yml` — B runner
- `docs/architecture.md` — design notes and operational rules

## Operational principles

- Never rewrite prior chat history.
- Only append when the last speaker check says it is this workflow's turn.
- Fail closed on inconsistent state.
- Keep each personality isolated in its own workflow.
- Use `repository_dispatch` to hand off control to the opposite workflow.
- Manual stop is done by disabling Actions, removing workflow files, or stopping dispatches.

## Current status

This repository was initialized from empty state and now contains the first design scaffold. The next commits add the core files needed for the first working prototype.
