#!/usr/bin/env bash

# qwen_loop.sh
# Runs your Qwen CLI in a loop until "TASK_COMPLETE" is found in the output

# ────────────────────────────────────────────────
#          ←←← CHANGE THIS LINE ACCORDING TO YOUR TOOL →→→
LLM_COMMAND="qwen"           # examples: qwen, qwen-cli, llm -m qwen2.5, etc.
# ────────────────────────────────────────────────

if [ $# -eq 0 ]; then
    echo "Error: No prompt provided."
    echo "Usage: $0 \"your main instruction/prompt text\""
    exit 1
fi

MAIN_PROMPT="$1"
MAX_ITERATIONS=10
ITERATION=1

echo "Starting loop with model command: $LLM_COMMAND"
echo "Prompt: $MAIN_PROMPT"
echo "Max iterations: $MAX_ITERATIONS"

while [ $ITERATION -le $MAX_ITERATIONS ]; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Iteration $ITERATION / $MAX_ITERATIONS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    PROMPT_WITH_ITER="Iteration $ITERATION: $MAIN_PROMPT"

    # Run the LLM command and capture both stdout and stderr
    OUTPUT=$($LLM_COMMAND "$PROMPT_WITH_ITER" 2>&1)
    EXIT_CODE=$?

    echo "$OUTPUT"

    if [ $EXIT_CODE -ne 0 ]; then
        echo "Warning: Command exited with code $EXIT_CODE"
    fi

    # Check for completion signal (case-insensitive)
    if echo "$OUTPUT" | grep -qi "TASK_COMPLETE"; then
        echo ""
        echo "✓ Completion signal found → stopping loop"
        exit 0
    fi

    echo "No completion signal. Sleeping 8 seconds..."
    sleep 8

    ((ITERATION++))
done

echo ""
echo "Reached max iterations ($MAX_ITERATIONS) without completion signal."
exit 1