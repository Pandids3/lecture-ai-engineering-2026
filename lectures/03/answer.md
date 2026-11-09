# Lecture 3 Answer

## Exercise

- Difference between Lecture 1 and Lecture 3:
  - Lecture 1 used `app.ask`, which made a plain LLM call without access to the course glossary. As a result, it could say that it did not know the answer or produce a plausible but unsupported answer.
  - Lecture 3 used `app.agent`, which could call tools. For the question about the three homework levels, the agent returned the correct levels: Basic, Implementation, and Advanced, and identified them as belonging to Lecture 1.

- Tool calls observed with `--trace`:
  - For the LoRA and QLoRA comparison, the agent called:
    - `search_glossary({"query": "LoRA"})`
    - `search_glossary({"query": "QLoRA"})`
  - It made 2 tool calls and required 2 model requests.
  - For the review-question request, it called:
    - `make_quiz({"lecture": 2})`
  - It made 1 tool call and required 2 model requests.

- Number of LLM calls:
  - The LoRA/QLoRA question used `requests=2`.
  - The review-question request also used `requests=2`.
  - The first request decided which tool to use, and the next request generated the final answer after receiving the tool result.

- Added tool:
  - I added `make_quiz(lecture: int)` to `app/tools.py`.
  - It selects a glossary term from the requested lecture and returns a JSON object containing a review question and its answer.
  - Its docstring explains that it should be used when the learner asks for a practice or review question.
  - I registered it in `app/agent.py` with `agent.tool_plain(tools.make_quiz)`.

- Verification:
  - Command: `uv run pytest -q`
  - Result: `15 passed`.

## Homework

### Basic

- Level completed: Basic.

- What I did:
  - I changed only the `search_glossary` tool docstring.
  - The original docstring instructed the model to put only one term in the query.
  - I changed it to suggest using several terms when comparing concepts.
  - I ran the same question with `--trace` before and after the change:
    `What is the difference between LoRA and QLoRA?`

- Results:
  - Original docstring:
    - Tool calls: `search_glossary("LoRA")` and `search_glossary("QLoRA")`.
    - Tool calls: 2.
    - Model requests: 2.
  - Modified docstring:
    - Tool call: `search_glossary("LoRA and QLoRA")`.
    - Tool calls: 1.
    - Model requests: 2.
  - The final answer was correct in both cases.

- Observations:
  - The tool docstring influenced the model's arguments and the number of tool calls.
  - Combining terms reduced the number of searches, but separate searches may provide more precise evidence.
  - The number of model requests did not change because the agent still needed one request to select the tool and another to produce the final answer.

### Implementation

- Level completed: Implementation.

- What I did:
  - I added `save_learning_log(topic: str, reflection: str)` to `app/tools.py`.
  - The tool saves learning records as JSONL in `learning_log/learning_log.jsonl`.
  - I registered the tool in `app/agent.py` with `requires_approval=True`.
  - I added `DeferredToolRequests` to the agent output type.
  - I updated the CLI to ask the user for approval and continue with the approval result.
  - I added a `TestModel` test to verify that saving requires approval.

- Results:
  - The agent displayed the tool name and arguments before saving.
  - When I answered `n`, the record was not saved.
  - When I answered `y`, the JSONL file was created with a timestamp, topic, and reflection.
  - The final test result was:

    ```text
    15 passed in 4.44s
    ```

- Observations:
  - Approval acts as a safety gate before an irreversible file-writing operation.
  - The tool body executes only after approval.
  - After adding an instruction explaining that a denied save must not be requested again, the agent correctly reported that nothing had been saved.
  - This pattern is useful for tools that write files, send messages, or perform other actions that are difficult to undo.