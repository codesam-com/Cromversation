# Architecture

## Core loop

Aurora → Boreal → Aurora → ...

Each workflow:
1. Checks if it is its turn
2. Reads full chat history
3. Calls GitHub Models
4. Appends a new block
5. Commits
6. Dispatches the other workflow

## Why repository_dispatch

Push events triggered by GITHUB_TOKEN do not trigger new workflows.
Only repository_dispatch and workflow_dispatch can chain executions.

## Model usage

Uses GitHub Models via REST API:
- no external API key
- runs inside Actions
- requires models: read permission

## Chat file rules

Each message block:

Personalidad:
mensaje

---

Never rewrite history. Only append.

## Safety

- Strict turn validation
- Reject invalid formats
- Reject duplicate turns
- Concurrency group avoids race conditions

## Start conversation

Manually trigger workflow:
- Personality A (Aurora)

## Stop conversation

- Disable workflows
- Delete workflow files
- Or stop dispatch chain
