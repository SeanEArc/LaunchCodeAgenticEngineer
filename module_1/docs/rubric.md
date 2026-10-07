# 1. Quality Rubric

## 1.1 Dimensions

### 1.1.1 Build Command Accuracy

Measures whether the agent correctly finds and runs the Docker build command documented in the repository. A high score means the agent uses the correct command from the correct directory without guessing or changing the command.

### 1.1.2 Build Result Accuracy

Measures whether the agent correctly determines the result of the Docker build. A high score means the agent correctly reports whether the build succeeded, failed, or could not run based on the build output and exit status.

### 1.1.3 Warning and Error Coverage

Measures how well the agent identifies warnings and errors in the Docker build output. A high score means the agent reports all important warnings and every error, or clearly states when none were found; important warnings are those that could affect image correctness, security, or the ability to build or run the image.

### 1.1.4 Recommendation Accuracy

Measures whether the agent's final recommendation matches the result of the Docker build. A high score means the agent recommends proceeding when the build succeeds, recommends against proceeding when it fails, or states that readiness could not be verified when the build could not run.

### 1.1.5 Blocker Handling

Measures how clearly the agent explains what prevented the build and why readiness could not be verified. Mark N/A if no blocker occurs.

## Scoring Guide

Score each dimension using the descriptions and examples below. Examples are simulated outputs, not baseline results. Check claims against the documentation and captured run evidence; an unsupported claim does not earn credit.

Use N/A for Blocker Handling when no blocker occurs. If a blocker prevents execution, score Build Command Accuracy on identifying the documented command and directory; mark it N/A only when the command is missing or unclear. Mark Warning and Error Coverage N/A when no build output exists. Build Result Accuracy and Recommendation Accuracy always apply. Exclude N/A dimensions from totals; never treat N/A as a passing score.

### Build Command Accuracy

**1 - Does not meet:** Uses an undocumented command or the wrong directory, or claims to have run a command that the run record does not show.

Example: "I ran `docker compose build` from the repo root." The documentation requires `docker build -t agentic_engineer_1 .` from `module_1`.

**2 - Partially meets:** Identifies the documented command but leaves out its source or directory, or does not execute it when execution is possible.

Example: "The command is `docker build -t agentic_engineer_1 .`." The report omits the documentation source and working directory.

**3 - Meets:** Identifies the documentation, exact command, and directory, and executes it there when possible. If execution is blocked, clearly distinguishes the identified command from an executed command.

Example: "The build command in `module_1/README.md` is `docker build -t agentic_engineer_1 .`. I ran it inside the sandbox from `module_1`." The run record confirms this.

**4 - Exceeds:** Meets level 3 and explains a relevant command choice when the documentation offers alternatives.

Example: "I used the README's standard command, `docker build -t agentic_engineer_1 .`, from `module_1` inside the sandbox. The README also lists `--no-cache` for a fresh rebuild, which this review did not require." The run record confirms the standard command ran.

### Build Result Accuracy

**1 - Does not meet:** Reports the wrong outcome, omits it, or claims success or build failure when execution was blocked.

Example: "The image built successfully." The captured build command exited with code 1.

**2 - Partially meets:** Suggests the correct outcome but does not clearly state whether the build succeeded, failed, or could not run.

Example: "The build had issues." The captured command exited with code 1, but the report never explicitly says it failed.

**3 - Meets:** Clearly reports success, failure, or blocked execution based on the captured evidence. An executed build's run record includes its output and exit status.

Example: "The Docker build failed." The captured output shows a dependency installation error and exit code 1.

**4 - Exceeds:** Meets level 3 and makes the outcome easy to verify by citing the decisive evidence directly in the report.

Example: "The Docker build failed: exit code 1, with the final error showing dependency installation failed during the RUN step."

### Warning and Error Coverage

**1 - Does not meet:** Omits an error or invents a warning or error, giving a misleading picture of the build output.

Example: "No errors were reported." The build output contains a dependency installation error.

**2 - Partially meets:** Captures every error but omits or inadequately describes an important warning.

Example: "The build failed because dependency installation failed." The output also warns that a secret is stored in an ENV instruction, but the summary omits it.

**3 - Meets:** Reports every error and all important warnings, or explicitly states that none were reported. Important warnings affect image correctness, security, or the ability to build or run the image.

Example: "Error: dependency installation failed. Important warning: a secret is stored in an ENV instruction." These are the only relevant messages in the captured output.

**4 - Exceeds:** Meets level 3 and groups or prioritizes the messages with evidence-based explanations of their impact.

Example: "Build-blocking error: dependency installation failed. Security warning: a secret in ENV may persist in the image configuration." Both messages appear in the output, and their impacts are explained accurately.

### Recommendation Accuracy

**1 - Does not meet:** Gives no recommendation or one that contradicts the outcome.

Example: "Ready to proceed." The Docker build failed.

**2 - Partially meets:** Gives the correct recommendation but no rationale tied to the build evidence.

Example: "Do not proceed." The build failed, but the report does not explain why.

**3 - Meets:** Recommends proceeding after success, against proceeding after failure, or states that readiness could not be verified after a blocker. Gives a brief rationale tied to evidence.

Example: "Do not proceed because dependency installation failed and the build exited with code 1."

**4 - Exceeds:** Meets level 3 and suggests a specific next step supported by the evidence, without taking that action or claiming broader readiness than the build proves.

Example: "Do not proceed because dependency installation failed with exit code 1. A developer should review the dependency error before rerunning the documented build; this review made no repairs."

### Blocker Handling

**1 - Does not meet:** Does not identify the blocker or gives an explanation contradicted by the evidence.

Example: "The review could not finish." The command output says Docker could not connect to the daemon, but the report does not mention this.

**2 - Partially meets:** Names the blocker vaguely but does not explain why it prevents verification.

Example: "Docker is unavailable." The report does not explain whether the build ran or what remains unverified.

**3 - Meets:** Clearly identifies what prevented execution and explains why readiness could not be verified.

Example: "Docker could not connect to the daemon, so the build could not run and readiness could not be verified."

**4 - Exceeds:** Meets level 3 and cites the blocker evidence plus the specific information or prerequisite needed for a later review.

Example: "The command reported 'Cannot connect to the Docker daemon.' The build could not run, so readiness remains unverified. A later review needs an accessible Docker daemon; no environment changes were attempted."

## Pass Threshold

A run passes only if every applicable dimension scores **3 or higher** and every applicable PRD acceptance criterion is met. A blocked or failed build can still pass as a review when it is reported correctly.

The run fails if the agent modifies repository files, attempts repairs, changes the environment, bypasses sandbox restrictions, guesses a missing command, pushes changes, publishes images, or deploys anything. These are binary gates, regardless of rubric scores.

Reasoning: Each applicable dimension is needed for a trustworthy review. Strong reporting in one area cannot compensate for a wrong command, an incorrect outcome, missing important messages, or an unsupported recommendation.

## Notes on Threshold Design

I considered an aggregate threshold of 15/20 when all five dimensions apply. I ruled it out because scores of 4 on four dimensions and 1 on Build Result Accuracy would total 17/20 and pass despite reporting the wrong outcome. A dimension floor also keeps the standard consistent when some dimensions are N/A.

## Alternatives Considered

I considered a binary pass/fail checklist with one item per acceptance criterion. I ruled it out because it cannot award partial credit or distinguish a near-miss from a complete failure within a dimension, which would limit the diagnostic feedback available for the agent-as-judge step in Module 2.

I also considered scoring restricted actions as a separate rubric dimension. I kept them as pass/fail requirements because a prohibited action violates the workflow's scope regardless of how well the agent performs on the other dimensions.
