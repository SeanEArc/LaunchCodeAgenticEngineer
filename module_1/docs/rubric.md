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

## 1.2 Alternatives Considered

I considered a binary pass/fail checklist with one item per acceptance criterion. I ruled it out because it cannot award partial credit or distinguish a near-miss from a complete failure within a dimension, which would limit the diagnostic feedback available for the agent-as-judge step in Module 2.

I also considered scoring restricted actions as a separate rubric dimension. I kept them as pass/fail requirements because a prohibited action violates the workflow's scope regardless of how well the agent performs on the other dimensions.
