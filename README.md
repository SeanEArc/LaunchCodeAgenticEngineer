# LaunchCodeAgenticEngineer

LaunchCode **Agentic Engineer** course materials. Each module is a self-contained Docker
development environment that builds on the previous one, pairing a pre-configured Python 3.12
image with the Claude Code CLI and the exercises for that part of the course.

## Repository structure

```text
.
├── module_1/   Base Docker environment + agent fundamentals
├── module_2/   Adds MCP servers, skills, and subagents
└── module_3/   Adds multi-agent orchestration, tool scoping, and an eval harness
```

Each module directory holds its own `Dockerfile`, `requirements.txt`, `settings.json`,
`statusline.sh`, and a `README.md` with the build and run commands for that module. Start with
the README inside the module you are working on — this file is only a map of the repository.

### module_1 — Environment and fundamentals

The base image: Python 3.12, the Anthropic SDK, Streamlit, Gmail/Slack client libraries, and the
Claude Code CLI. Also contains the parallel agent-session exercise:

| Path | Purpose |
| --- | --- |
| `module_x.py` | Business-rule utilities — the "Session A" target (write tests, don't edit the file) |
| `module_y.py` | Formatting and reporting utilities — the "Session B" target (improve docs, don't edit tests) |
| `agent_docker_check.md` | Prompt for having an agent verify the Docker build |

See [module_1/README.md](module_1/README.md).

### module_2 — MCP servers, skills, and agents

Extends module 1 with Slack and Gmail MCP servers and the Claude Code customization layer:

| Path | Purpose |
| --- | --- |
| `skills/` | Slash commands: `check-gmail`, `send-email`, `send-slack-message`, `summarize-session` |
| `agents/` | Subagent definitions: `code-reviewer`, `email-summarize` |
| `sample_docs/` | Example PRD, rubric, and iteration log used by the exercises |
| `sample_review.py` | Sample code used as input for the `code-reviewer` agent |

See [module_2/README.md](module_2/README.md).

### module_3 — Orchestration, tool scoping, and evaluation

Extends module 2 with a multi-agent pipeline and the tooling used to measure it:

| Path | Purpose |
| --- | --- |
| `agents/` | Role definitions: `planner`, `implementer`, `reviewer`, `code-reviewer`, `docs-reviewer`, `project-manager`, `email-summarize` |
| `mcp/` | `coursetools`, `retrieval`, and `storage` MCP servers; `roles.allowlist.json` scopes each tool to the roles allowed to call it |
| `eval/` | Eval harness: `orchestrator.py`, `run_regression.py`, `run_holdout.py`, `analyze_routing.py`, `rubric.json`, and the deterministic/rubric test suites |
| `docs/` | PRD, routing and tool-grant map, holdout task set, calibration and iteration logs, quality reports |
| `.eval-artifacts/` | Baseline and per-run transcripts produced by the eval harness |
| `.memory/` | Reference notes the agents retrieve during runs |

See [module_3/README.md](module_3/README.md).

## Getting started

Clone the repository and build the module you need:

```bash
git clone https://github.com/LaunchCodeEducation/LaunchCodeAgenticEngineer.git
cd LaunchCodeAgenticEngineer/module_1
docker build -t agentic_engineer_1 .
docker run -it --rm -v claude-auth:/claude-auth -p 8501:8501 -v "$PWD":/workspace agentic_engineer_1
```

Pre-built images are published automatically for each module, so you can skip the build:

```bash
docker run -it --rm -v claude-auth:/claude-auth -p 8501:8501 -v "$PWD":/workspace \
  us-central1-docker.pkg.dev/hire-human/hire-human-ai/agentic_engineer_1:latest
```

Replace `agentic_engineer_1` with `agentic_engineer_2` or `agentic_engineer_3` for later modules;
those images need additional ports and environment variables, documented in their own READMEs.

> **Claude authentication:** the `-v claude-auth:/claude-auth` named volume persists your Claude
> Code login across container runs and across every module. You log in once and every later
> container reuses that credential.
