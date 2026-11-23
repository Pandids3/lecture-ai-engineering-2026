# Lecture 5: Retrieval, Context, and Evidence

## Exercise

The experiment used `gemini-3.5-flash-lite` with the pinned course dependencies on Windows and Python 3.13.1. The course RAG update was integrated before measurements began. The quiz and approval-protected learning-log tools from Lecture 3 were preserved. The normal agent exposed five tools in both homework conditions, although every successful normal-mode run used only `search_materials`.

The comparison question was:

> According to Lecture 2, which weights does LoRA keep fixed, what does it train, and what does QLoRA add? Answer in English and cite the lecture PDF pages.

Vector retrieval, Tree, and Graph were configured for the 214 pages of the main lectures from Lectures 1–3. Full context included all nine documents and 438 pages in the supplied JSON. This difference prevents a strict comparison under identical document coverage. All exercise attempts below were made with `RAG_TOP_K = 5`.

| Method | Answer and evidence | Time (s) | Input / output tokens | Model responses | Estimated generation cost (USD) |
|---|---|---:|---:|---:|---:|
| Full context | Failed with `ModelAPIError: ReadError` after preparing 228,082 input characters. No completed answer or usage summary. | Not available | Not available | Not available | Not available |
| Vector retrieval | Correct explanation of fixed W, trainable A and B, and 4-bit quantization; cited Lecture 2, pp. 51–52. | 9.96 | 3,842 / 172 | 2 | 0.001583 |
| Tree | Failed with HTTP 503; no completed answer, traversal trace, or usage summary. | Not available | Not available | Not available | Not available |
| Graph | Correct, with citations to Lecture 2, pp. 51–52. | 15.35 | 5,796 / 182 | 2 | 0.002194 |

Vector retrieval made one `search_materials` call with `query = "LoRA 固く固定 訓練 QLoRA"`. Independently replaying that query returned Lecture 2 pages 52, 51, 60, 54, and 61. Pages 51–52 support the answer: the pretrained weights W remain fixed, low-rank matrices A and B are trained, and QLoRA quantizes the original weights to 4 bits.

Graph made one `search_graph` call with `query = "LoRA QLoRA weights train fix"`. Its independent replay also contained the cited evidence. For this question, Graph consumed more input tokens, took longer, and had a higher estimated generation cost than vector retrieval. This single observation does not establish a general ranking.

The full-context failure was a read error, not a confirmed context-window limit. The Tree error indicates service unavailability and does not establish a retrieval failure. Unavailable usage and cost are not treated as zero.

Original CLI output and diagnostic records: [vector](evidence/k5-q1.json), [full context](evidence/full-q1.json), [Tree](evidence/tree-q1.json), and [Graph](evidence/graph-q1.json).

## Homework

**Selected level: Basic.**

I changed `RAG_TOP_K` in `app/config.py` from **5 to 3**. This limits pages returned by each vector search, rather than the number of searches an agent may perform. No index rebuild was required.

The purpose was to determine whether fewer results could preserve the required evidence while reducing context consumption. The model, source documents, index, instructions, tool descriptions, and available tools remained unchanged between conditions. Each question started a fresh agent process without conversation history. No temperature or seed override was applied.

### Questions and expected evidence

- **Q1:** According to Lecture 2, which weights does LoRA keep fixed, what does it train, and what does QLoRA add? Answer in English and cite the lecture PDF pages.
- **Q2:** According to Lecture 3, how does compaction differ from memory across sessions, and are all daily notes transferred to long-term memory? Answer in English and cite the lecture PDF pages.
- **Q3:** What were the measured average response time and accuracy of our RAG system in today's experiments? Answer in English using only the lecture materials.

Q1 requires fixed original weights, trainable A and B, and 4-bit quantization, supported by Lecture 2, pp. 51–52. Q2 requires the distinction between within-session compaction and external memory, plus selective promotion of daily notes, supported by Lecture 3, pp. 39–40. Q3 should acknowledge that the materials contain no measurements of this particular system.

Page references use the supplied Japanese course dataset. Translated or expanded PDFs may have different page numbers.

### Measured comparison

| Question | Results per search | Search calls | Model responses | Time (s) | Input / output tokens | Estimated generation cost (USD) |
|---|---:|---:|---:|---:|---:|---:|
| Q1 | 5 | 1 | 2 | 9.96 | 3,842 / 172 | 0.001583 |
| Q1 | 3 | 1 | 2 | 4.92 | 2,885 / 156 | 0.001256 |
| Q2 | 5 | 1 | 2 | 5.79 | 3,293 / 230 | 0.001563 |
| Q2 | 3 | 2 | 3 | 8.96 | 5,662 / 257 | 0.002341 |
| Q3 | 5 | 1 | 2 | 13.35 | 4,040 / 131 | 0.001540 |
| Q3 | 3 | 1 | 2 | 7.19 | 2,928 / 104 | 0.001138 |

There is one completed observation per question and condition. The execution order was Q1–Q3 at k=5, the additional exercise methods, and Q1–Q3 at k=3. The first k=3 attempt for Q1 failed with HTTP 503; the first attempt for Q2 failed with `ReadError`. Both were retried using the same question, model, and configuration. Their records are retained as [Q1 attempt 1](evidence/k3-q1-attempt1.json) and [Q2 attempt 1](evidence/k3-q2-attempt1.json). The table reports completed runs and excludes unavailable usage from failures rather than assigning zero cost.

Time includes search and query embedding during the agent run. Token usage is summed across model responses. Estimated generation cost excludes embeddings, index construction, diagnostic replays, and unreported usage from failed attempts.

### Changes in calls, answers, and evidence

**Q1: the smaller result set retained the evidence.** Both conditions correctly described LoRA and QLoRA and cited Lecture 2, pp. 51–52. At k=3 the agent searched for `LoRA QLoRA weights`; the replay returned pages 52, 51, and 60. Input tokens fell by 24.9%, and estimated generation cost fell from USD 0.001583 to USD 0.001256. The model generated different search wording between conditions, so this is an end-to-end comparison rather than a fixed-query retrieval benchmark. Records: [k=5](evidence/k5-q1.json) and [k=3](evidence/k3-q1.json).

**Q2: the smaller result set required another search.** Both runs first searched for `compaction memory across sessions daily notes long-term memory`. At k=5, the replay returned Lecture 3 pages 65, 39, 38, 40, and 13. At k=3, it returned pages 65, 39, and 38, omitting page 40's explanation of daily-note selection. The agent then searched for `daily notes long-term memory`, whose replay returned pages 40, 38, and 13.

Both completed answers correctly distinguished compaction from persistent memory and explained that not every daily note becomes long-term memory. Both cited pp. 39–40. However, k=3 required two searches and three model responses. Input tokens increased by 71.9%, elapsed time increased, and estimated generation cost rose from USD 0.001563 to USD 0.002341. Fewer results per search therefore did not produce a cheaper complete interaction. Records: [k=5](evidence/k5-q2.json) and [k=3](evidence/k3-q2.json).

**Q3: both conditions declined to invent measurements.** The k=5 query was `average response time accuracy RAG system experiments`; the k=3 query was `response time accuracy RAG system experiments`. Both answers stated that the requested measurements were absent. Both referred to Lecture 2, p. 13 for general evaluation advice, without presenting its illustrative example as our measured performance. Input tokens fell by 27.5%, and estimated generation cost fell from USD 0.001540 to USD 0.001138. Records: [k=5](evidence/k5-q3.json) and [k=3](evidence/k3-q3.json).

### Findings and limitations

The six completed answers met the stated expectations when checked against the supplied page text. Across the three completed questions, total input tokens increased from 11,175 to 11,475, and estimated generation cost increased from USD 0.004686 to USD 0.004735. Q2's additional search outweighed the savings on Q1 and Q3.

The committed value of 3 is the evaluated homework variant. These observations do not establish it as a better default. For questions requiring evidence from several pages, the five-result setting deserves further evaluation before being replaced. A larger question set and repeated, interleaved trials would be needed to estimate reliability, average latency, and cost. The intermittent API failures make timing comparisons particularly uncertain.

Retrieval replays in the evidence JSON files are explicitly labelled independent diagnostics. They inspect complete page text because the CLI abbreviates tool returns. They are not captures of the original tool-return payloads, and their API calls are excluded from recorded agent timings and generation costs. The source and index were unchanged during these checks.

The main lesson is to evaluate context across the entire interaction. Reducing the text returned by one search can increase the number of searches and model responses needed to produce a grounded answer.

### Reproduction and validation

Configure the existing `GEMINI_API_KEY` environment variable and run from the repository root:

```bash
uv sync --frozen
uv run python -m app.agent --list-tools
uv run python -m app.agent --trace "According to Lecture 2, which weights does LoRA keep fixed, what does it train, and what does QLoRA add? Answer in English and cite the lecture PDF pages."
uv run pytest -q
git diff --check
```

For the before/after comparison, run each exact question above with `RAG_TOP_K = 5`, then change only that setting to 3 and repeat. Keep documents and model unchanged. For the exercise comparison, use the Q1 command with `--full-context`, `--tree`, or `--graph` before changing the setting. The JSON files preserve the actual questions, flags, configuration, CLI output, exit status, and replayed retrieval results.

Validation completed with **22 tests passing**, successful Python syntax checks for the integration changes, and no whitespace errors. The tool listing confirmed preservation of the earlier tools and the learning-log approval requirement. AI assistance was used to integrate the course update, execute the experiments, inspect evidence, and prepare this report. Every numerical result above comes from a recorded execution.
