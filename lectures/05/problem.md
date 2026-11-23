# Lecture 5 Exercise and Homework: Answering Questions with Retrieved Lecture Materials

## Learning objectives

- Run full-context and retrieval-based answering, and compare answers, supporting evidence, time, and token usage.
- Explain the page-based chunk structure and the differences between vector retrieval, Tree, and Graph.
- Adapt a retrieval method to your needs and compare its behavior before and after a change using the same questions.

This exercise builds on the model + loop + tools structure from Lecture 3 by changing how lecture materials are retrieved. Applying the evaluation principles from Lecture 4, check both the correctness of the answer and whether the cited pages actually support it.

## Materials and code

| File | Purpose |
|---|---|
| [data/rag_data/lectures.json](../../data/rag_data/lectures.json) | Titles and text organized by lecture, section, and page. Each page is one chunk. |
| [data/rag_data/tree.json](../../data/rag_data/tree.json) | The document, section, and page hierarchy. |
| [data/rag_data/graph.json](../../data/rag_data/graph.json) | Page and term nodes, together with their relationships. |
| [data/rag_data/index.sqlite3](../../data/rag_data/index.sqlite3) | The search database containing 214 pages from the main materials for Lectures 1–3. |
| [scripts/build_rag_index.py](../../scripts/build_rag_index.py) | Creates document embeddings and builds the SQLite search database. |
| [app/retrieval.py](../../app/retrieval.py) | Vector retrieval, Tree traversal, Graph traversal, and full-context processing. |
| [app/tools.py](../../app/tools.py) | Tool descriptions, inputs, and outputs exposed to the model. |
| [app/agent.py](../../app/agent.py) | Instructions, tool registration, and execution modes. |
| [app/config.py](../../app/config.py) | Settings for document scope, result counts, and Graph traversal. |

**Current document scope:** Vector retrieval, Tree, and Graph use the 214 pages of the main materials for Lectures 1–3. Full context uses all nine documents and 438 pages in the materials JSON. This exercise examines different retrieval paths. Before drawing conclusions about which method performs better under equivalent conditions, align their document coverage.

## Preparation

### 1. Incorporate the Lecture 5 update and create the lec05 branch

After the Lecture 5 update is published in the course repository, select **Sync fork → Update branch** in your own fork, then run the following in the Codespaces terminal:

```bash
git switch main
git pull --no-rebase
git switch -c lec05
uv sync --frozen
```

- If `lec05` already exists, switch to it with `git switch lec05`.
- If uncommitted changes from an earlier lecture prevent switching branches, commit those changes on their current branch before trying again.
- If updating produces merge conflicts, preserve your changes and consult the instructor.

Use the same `GEMINI_API_KEY` environment variable as in Lecture 1. If you added the Codespaces secret after starting the Codespace, restart it. See the [README](../../README.md) for setup instructions.

### 2. Check the included search database

Vector retrieval and Graph use the supplied `data/rag_data/index.sqlite3` directly. Once the Lecture 5 update is incorporated, proceed to the exercise. Query embeddings and answer generation require `GEMINI_API_KEY`. Tree and full context do not require the search database.

## Exercise

### STEP 1: Answer using all materials at once

First, assign the comparison question to a variable in the terminal. Reuse this exact question for each method below.

```bash
AIE_QUESTION='According to Lecture 2, what does LoRA keep fixed, what does it train, and what does QLoRA add?'
uv run python -m app.agent --full-context --trace "$AIE_QUESTION"
```

Record the answer, cited pages, and the final `[time]`, `[usage]`, and `[cost]` values in [answer.md](answer.md).

Full context may answer correctly. Examine the actual result rather than assuming it will fail. Distinguish an input-limit error from a case in which the input is accepted but the model fails to use the necessary evidence.

### STEP 2: Inspect retrieval results independently

```bash
uv run python -m app.retrieval "LoRA QLoRA differences"
```

This retrieves pages similar to the query without running the agent. The original configuration returns up to five results; the actual limit is controlled by `RAG_TOP_K`. Each result includes the lecture title, section, page title, PDF page number, and text.

- Do the results include a page that supports the answer, such as Lecture 2, PDF p. 52?
- Can you distinguish pages that merely contain related terminology from pages that provide the required evidence?

Open the materials JSON in the editor and search for an identifier such as `lec02-main-p052` to inspect the corresponding page text.

### STEP 3: Answer using retrieved materials

```bash
uv run python -m app.agent --trace "$AIE_QUESTION"
```

The normal execution mode uses an agent with `search_materials(query)`. The model chooses the search terms and answers using the returned text.

- Inspect `[tool call]` entries to identify the search terms and number of tool calls.
- Check whether each citation in the form "Lecture N, PDF p. N" supports the associated explanation.
- Distinguish failure to retrieve evidence from failure to use evidence that was retrieved.

For some questions, p. 52 alone provides sufficient evidence. Increasing the number of cited pages is not an objective in itself.

### STEP 4: Answer the same question with Tree and Graph

Tree selects pages by following the table of contents.

```bash
uv run python -m app.agent --tree --trace "$AIE_QUESTION"
```

It uses only `browse_tree(node_id)`. The agent first obtains the lecture list, then follows returned identifiers through lectures, sections, and pages. Page candidates in `children` contain only the first sentence of the page text. Passing a page identifier returns the complete text in `node.content`. When a page has no sentence-ending punctuation recognized by the implementation, its candidate text is the first line. Inspect the trace to see the selected sections and the pages whose full text was retrieved.

Graph begins with vector search and expands the surrounding candidates.

```bash
uv run python -m app.agent --graph --trace "$AIE_QUESTION"
```

It uses `search_graph(query)`. The top three search results serve as starting pages. The method follows adjacent-page and shared-term relationships for up to two hops and returns the text of at most ten pages, including the starting pages. Moving directly to an adjacent page is one hop; moving from a page through a term to another page is two hops. Sharing a term does not guarantee that a page contains the answer.

Record how Tree and Graph affect the answer, supporting citations, elapsed time, and input token usage.

### STEP 5: Compare and record the results

Summarize the results for each method in the table in `answer.md`.

| Output | Meaning |
|---|---|
| `[time]` | Seconds until the answer is complete, including retrieval and embedding. |
| `[usage]` | Total input tokens, output tokens, and model responses for one question. |
| `[cost]` | Estimated generation API cost. Query embeddings and index construction are excluded. |

If the cost cannot be calculated, record it as unavailable rather than zero.

If time permits, repeat the comparison with other questions. Keep separate results for each question.

| Type | Example question | Evidence to check |
|---|---|---|
| Multiple pages | In the Lecture 3 examples, how does compaction differ from memory across sessions? Are all daily notes transferred to long-term memory? | Lecture 3, PDF pp. 13, 39, and 40. |
| Not in the materials | What are the measured average response time and accuracy of the RAG system built in this exercise? | The lecture materials do not contain measurement logs for this system. |

### STEP 6: Submit your work and stop Codespaces

Write your exercise results in `lectures/05/answer.md` and open a PR from your working branch to `main` in your own fork. **Verify that the PR's base repository is your own fork.**

```bash
git add lectures/05/answer.md
# Also stage any code files you changed.
git commit -m "Complete Lecture 5 exercise and homework"
git push -u origin lec05
```

Do not commit API keys or experimental search databases. Finally, select **Stop Current Codespace** from the Codespaces menu in the lower-left corner.

## Homework: complete any one level

Choose Basic, Implementation, or Advanced. **Completing any one level satisfies the homework requirement.** In the Homework section of the same `answer.md`, state the selected level, what you changed, the results, and your observations or questions.

| Level | Task |
|---|---|
| Basic | Change one instruction, tool description, or retrieval result count. Run the same question with `--trace` and compare the behavior before and after the change. |
| Implementation | Improve one retrieval step, such as including the full text of adjacent pages, and compare it with ordinary retrieval. |
| Advanced | Improve Tree, Graph, or a combination of methods. Define the questions you want to answer and compare your method with Basic RAG using the same questions. |

### Basic level

Change only one of the following at a time:

- `INSTRUCTIONS` in `app/agent.py`. When using Tree or Graph, use `TREE_INSTRUCTIONS` or `GRAPH_INSTRUCTIONS`, respectively.
- A tool's docstring in `app/tools.py`.
- `RAG_TOP_K` in `app/config.py`, which controls the number of results returned by ordinary vector retrieval.

Keep the questions, model, and source materials identical. Compare the tools called, their arguments and call counts, the answers, and their supporting citations. Also record time, token usage, and estimated generation API cost. These changes alone do not require rebuilding the index.

### Implementation level

For example, modify `app/retrieval.py` to return the full text of one page before and after each retrieved page.

1. Use the page information from `load_pages()` to find adjacent pages with the same `document_id` as the search result.
2. Avoid returning duplicate pages, and include both the text and citation information.
3. Use the same questions as before the change. Identify cases where the modification adds necessary evidence and cases where it adds irrelevant information.
4. Record the implementation, comparison results, and remaining failures.

Other retrieval improvements suited to your intended use are also acceptable. If you change only the retrieval range without changing the document text or embedding settings, the index does not need to be rebuilt.

If you change the document text or embedding settings, follow the [README instructions](../../README.md#第5回講義資料を検索する), set `AIE_RAG_DB` to an experimental database path, and then build the index.

### Advanced level

1. Define the questions you want the system to answer. For example, choose explanations spanning sections or comparisons between related terms. Identify the supporting pages in advance.
2. Design the retrieval method. Options include changing how Tree returns the table of contents or candidate text, changing Graph relationship types, hop limits, or candidate selection, or combining retrieval methods.
3. Explain the data structure, storage, and retrieval method, together with your reasons for choosing them.
4. Compare with Basic RAG using the same questions, model, and document scope. Record the answers, supporting citations, time, token usage, and estimated generation API cost.
5. Include examples of improvements and failures, and discuss whether you would adopt the method for your intended use.

AI tools are permitted. Report what you actually executed and verified. Follow the course announcements for the submission deadline.

## Troubleshooting

| Symptom | What to check |
|---|---|
| `GEMINI_API_KEY` is missing | Check that the Codespaces secret is configured. Restart Codespaces if the secret was added after startup. |
| The search database is missing | Incorporate the Lecture 5 update and check that `data/rag_data/index.sqlite3` exists. If `AIE_RAG_DB` is set, check the specified path. |
| The API rate limit is reached | Wait as instructed by the message, then try again. |
| The question is reported as empty | If you opened another terminal, set `AIE_QUESTION` again in that terminal. |
| Retrieved results do not answer the question | Run retrieval independently with `app.retrieval`, and check the search terms, document scope, and result count. |
| Full context exceeds the input limit | Record the error and execution conditions, then try the other methods. Clearly mark any unexecuted results. |

The same question can produce different results across runs. Avoid judging an entire method from one success or failure. Check which evidence was retrieved and how it was used.
