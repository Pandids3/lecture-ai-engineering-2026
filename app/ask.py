"""第1回: 会話履歴を保ちながらLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールは使わず、会話履歴だけを保持する「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str, history: list[types.Content] | None = None) -> str:
    client = genai.Client(api_key=get_api_key())
    # If no history is provided, create a new conversation.
    # Reuse this list so each request includes the full conversation.
    conversation = history if history is not None else []
    # Gemini distinguishes user and model messages by their roles.
    conversation.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=question)],
        )
    )
    # Measure only the time spent waiting for the model response.
    started_at = time.perf_counter()
    response = client.models.generate_content(model=MODEL, contents=conversation)
    elapsed_seconds = time.perf_counter() - started_at

    usage = response.usage_metadata
    print(f"[tokens] input={usage.prompt_token_count}, output={usage.candidates_token_count}")
    print(f"[time] response_seconds={elapsed_seconds:.2f}")

    # Store the response so the next turn can take it into account.
    conversation.append(
        types.Content(
            role="model",
            parts=[types.Part.from_text(text=response.text)],
        )
    )
    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    question = args.question or DEFAULT_QUESTION
    history: list[types.Content] = []
    try:
        # Continue after the first question until the user presses Enter.
        while question:
            print(f"[質問] {question}\n")
            print(ask(question, history))
            question = input("\n次の質問（終了するにはEnter）: ").strip()
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
