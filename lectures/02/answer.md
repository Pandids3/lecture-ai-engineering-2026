# Session 2 Submission

## Practice

- Model and configuration used (from `result.json` → `config`): `Qwen/Qwen3.5-0.8B`, LoRA without quantization, seed `42`, `lora_r=16`, `lr=2e-4`, `num_train_epochs=20`, `lora_alpha=32`, `warmup_steps=6`, `max_seq_len=512`, `max_new_tokens=96`, and greedy generation (`do_sample=false`).
- Did I run the training myself (`executed_training_myself`): yes.
- Before training: `format_rate` = `0.0952` (2/21; 9.5%) / `content_rate` = `0.0000` (0/21; 0%).
- After training: `format_rate` = `1.0000` (21/21; 100%) / `content_rate` = `0.9048` (19/21; 90.5%).
- Regressed questions: none (`regressed = []`).
- Remaining failures after training and their type:
  - An unsupported question about when grades are released was answered with the FAQ deadline and `needs_review=false`; this is an unsupported assertion.
  - An unsupported question about whether office-hour reservations are required was answered using the office-hour schedule and `needs_review=false`; this is also an unsupported assertion.
- Knowledge-question results from section 6:
  - Unknown final-assignment deadline: `format_error` → `asserted`.
  - Instructor's name: `format_error` → `needs_review`.
  - Next lecture topic: `format_error` → `needs_review`.
  - FAQ control question about the assignment deadline: `format_error` → `asserted`.
- Training loss and training time: not included in the saved JSON files; these values must be copied from the training cell output in Colab.
- What changed and what did not change after training: LoRA changed the model's output behavior substantially. Format compliance improved from 9.5% to 100%, and content correctness improved from 0% to 90.5%. The model learned to produce the required JSON structure and usually reproduced FAQ answers. However, it still sometimes treated an unsupported question as if it were covered by a related FAQ entry. Therefore, the training improved the response format much more reliably than the model's ability to recognize missing knowledge.

## Homework

- Level completed: Basic.
- Configuration or data changed: `num_train_epochs` was changed from `20` to `10`. All other training and generation settings were kept unchanged, and the runtime was restarted before the second run.
- Results:

  | Configuration | `format_rate` before | `format_rate` after | `content_rate` before | `content_rate` after | Final logged loss | Training time | Regressions |
  |---|---:|---:|---:|---:|---:|---:|---|
  | 20 epochs | 9.5% | 100.0% | 0.0% | 90.5% | 0.01390 | 243.864 s (40 steps) | none |
  | 10 epochs | 9.5% | 100.0% | 0.0% | 85.7% | 0.09794 | 121.199 s (20 steps) | none |

  The final logged loss for the 20-epoch run was `0.0138996676`, with a training runtime of `243.8644` seconds over 40 steps. The final logged loss for the 10-epoch run was `0.0979359388`, with a training runtime of `121.199` seconds over 20 steps. The reported `train_loss` values (`0.4194521006` for 20 epochs and `0.8292546630` for 10 epochs) are average training losses over each run, not final logged losses.
- Reflection on when fine-tuning is and is not appropriate: In this experiment, both training durations achieved perfect format compliance, so ten epochs were already sufficient to learn the JSON structure. However, the twenty-epoch run achieved a higher content rate (90.5% versus 85.7%) and produced one additional correct test answer. This suggests that additional training improved some content behavior, but it did not eliminate unsupported assertions or guarantee reliable knowledge judgment. Fine-tuning is appropriate for stable behavior such as output format, tone, or repeated procedures. It is less appropriate for changing or externally sourced knowledge, where retrieval or RAG is usually safer.

### Implementation

- Level completed: Implementation.
- Configuration or data changed: The original course FAQ was replaced with a fictional university-library FAQ in English. The grounded questions, unsupported questions, knowledge questions, and system prompt were also rewritten for this topic. The LoRA configuration remained unchanged: `num_train_epochs=20`, `lr=2e-4`, `lora_r=16`, `lora_alpha=32`, `warmup_steps=6`, `seed=42`, and greedy generation.
- Verification of the saved files: `result_implementation.json` records the library questions, the expected 20-epoch/40-step configuration, and `executed_training_myself=true`. The corresponding before/after evaluation files contain 21 English library questions and are different from the original and Basic-level JSON files.
- Results:

  | Configuration | `format_rate` before | `format_rate` after | `content_rate` before | `content_rate` after | Final logged loss | Training time | Regressions |
  |---|---:|---:|---:|---:|---:|---:|---|
  | Implementation, 20 epochs | 100.0% | 100.0% | 33.3% | 95.2% | 0.01451 | 192.311 s (40 steps) | none |

  The final logged loss was `0.0145086944`, with `mean_token_accuracy=0.9938133`, `entropy=0.0203698`, and `grad_norm=0.1548642`. The average `train_loss` reported by the trainer was `0.3657277871`; this is different from the final logged loss because it averages the training loss over the run.
- Remaining failure: The unsupported question `Can I reserve a computer?` was answered with the unrelated grounded statement `Study Room B can be reserved online.` and `needs_review=false`. This is an unsupported assertion caused by reusing a related FAQ entry. All other 20 evaluation questions passed the content check, and no regressions were detected.
- Knowledge-question behavior: After training, the unsupported library questions requested confirmation with `needs_review=true`, while the control question about the borrowing period was answered as a grounded fact with `needs_review=false`. This indicates that the custom implementation improved the missing-knowledge behavior, although it did not eliminate every semantic confusion.
- Reflection: The Implementation level shows that the same LoRA procedure can be transferred to a new domain and language without changing the training algorithm. The model learned the library answer format and most of the new FAQ content. The remaining computer-reservation error is important: similar wording or related concepts can still cause the model to copy a nearby fact instead of recognizing that the FAQ does not provide the requested information. For a real library assistant, retrieval with explicit evidence checking would be safer than relying only on fine-tuning.
