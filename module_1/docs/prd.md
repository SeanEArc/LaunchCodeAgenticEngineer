# PRD (Product Requirements Document)

This workflow reviews a repository's Docker setup by running the documented build command, reporting the outcome, and recommending whether the repository is ready to proceed.

## Trigger

A developer manually starts a single-agent session in Claude Code from the `module_1` directory, which contains the Dockerfile and documented build command, then submits the review prompt from `agent_docker_check.md`; no automated hook initiates the workflow.

## Decision Events

- If the documentation does not provide a clear Docker build command, the agent stops and reports that the review cannot be completed without clarification.
- If Docker is unavailable or the sandbox prevents the build from running, the agent reports the blocker and states that readiness could not be verified; it does not change the environment or bypass restrictions.
- If the Docker build succeeds, the agent summarizes any warnings and recommends proceeding based on the successful build.
- If the Docker build fails, the agent reports the relevant error output and recommends against proceeding; it does not attempt a repair.

## Actions

1. Read the repository's documentation to identify the documented Docker build command.
2. Run the documented Docker build command from the `module_1` directory inside the sandbox.
3. Capture the build output and exit status.
4. Determine whether the build succeeded, failed, or could not run.
5. Summarize any warnings, errors, or blockers in the captured output.
6. Produce a final readiness recommendation with a brief rationale, stating when readiness could not be verified.

The agent does not modify repository files, attempt repairs, push changes, publish images, or deploy anything.

## Acceptance Criteria

A workflow run passes when all applicable criteria below are met; a failed or blocked Docker build can still be a successful review if it is reported accurately.

- The report identifies the documentation used, the exact documented build command, and the working directory; the run record shows that this command was executed inside the sandbox from `module_1` when execution was possible.
- For an executed build, the run record includes the captured build output and exit status, and the report correctly labels the build as successful or failed based on that evidence.
- The summary includes all important warnings and every error present in the captured build output. Important warnings are those that could affect image correctness, security, or the ability to build or run the image. If no important warnings or errors are present, the summary explicitly states that none were reported.
- A successful build receives a recommendation to proceed, while a failed build receives a recommendation against proceeding; each recommendation includes a rationale tied to the build evidence.
- If the documented command is missing or unclear, the agent stops without guessing a command, identifies the missing information, and states that readiness could not be verified.
- If Docker is unavailable or the sandbox blocks execution, the report identifies the blocker and states that readiness could not be verified without claiming that the image built successfully or failed.
- The run record shows no repository file modifications, repair attempts, environment changes, attempts to bypass sandbox restrictions, pushes, image publishing, or deployments.
