# Session 1: Answers juanleon2207

## Exercises

### Course-specific question

Question:

> What are the 3 levels of homework in the AIE2026 course?

Model answer summary:

The model gave a generic classification: fundamentals, intermediate, and extension. It presented these as a typical AIE2026 structure, but it did not know the actual course definition.

Observation:

This is an example of a hallucination caused by asking a bare LLM about course-specific information that is not included in its context.

### Token count

Model: `gemini-3.5-flash-lite`

| Question | Input tokens | Output tokens |
|---|---:|---:|
| What is LoRA? (run 1) | 6 | 645 |
| What is LoRA? (run 2) | 6 | 708 |
| What is LoRA? (run 3) | 6 | 688 |
| What are the 3 levels of homework in the AIE2026 course? | 19 | 275 |

## Homework: Basic Level

Tasks performed:

- Asked the same general question, What is LoRA?, three times.
- Recorded the input and output token counts for each run.
- Compared the generated answers with the course definition.

Results:

All three LoRA answers were generally correct and explained low-rank adaptation, frozen base-model weights, trainable adapter matrices, and the benefits of parameter-efficient fine-tuning. However, the wording, examples, and level of detail changed between runs. The output token counts varied from 645 to 708 and 688, while the input count stayed at 6.

Observations:

The same prompt can produce different answers because the output is probabilistic. An LLM can explain common topics such as LoRA, but it can invent a plausible answer about information that is not in its training data.

## Homework: Implementation Level

Tasks performed:

- Modified `app/ask.py` to preserve conversation history between turns.
- Stored user messages with the `user` role and model responses with the `model` role.
- Added an interactive loop that accepts follow-up questions until the user presses Enter.

Results:

The conversation was tested with two turns. The first request asked the model to remember that the user's name was Ana. The second request asked for the user's favorite color, after stating that it was green. The model answered that the favorite color was green and remembered the name Ana.

The first turn used 11 input tokens and 12 output tokens. The second turn used 40 input tokens and 8 output tokens. The higher input count on the second turn shows that the previous conversation was included in the request.

Observations:

Conversation history allows the model to answer follow-up questions using earlier context. However, the full history is sent with every request, so input token usage increases as the conversation grows.

## Homework: Advanced Level

Tasks performed:

- Added response-time measurement to `app/ask.py` using `time.perf_counter()`.
- Recorded input tokens, output tokens, and API response time for multiple questions.
- Considered the relationship between token usage, response time, and API rate limits.

Results:

Model: `gemini-3.5-flash-lite`

| Question | Input tokens | Output tokens | Response time |
|---|---:|---:|---:|
| Explain LoRA in one sentence. | 8 | 38 | 2.26 s |
| What are the three homework levels in the AIE2026 course? | 17 | 81 | 0.81 s |

The general question produced a correct explanation of LoRA. The course-specific question used more input and output tokens, but the model correctly stated that it did not have access to the private course information. Response time did not increase directly with token count in this small test: the shorter answer took longer.

Observations:

Measuring both tokens and latency gives a better view of API usage than measuring. Longer conversation histories increase input-token usage and may increase cost. 