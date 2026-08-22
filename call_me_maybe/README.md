*This project has been created as part of the 42 curriculum by danmorei*

# Description

Call-Me-Maybe is a project part of the 42 curriculum to create a function calling engine, that will take a natural-language request and a catalogue of available functions and produces the function that should be called along with its typed arguments. It does not answer the question. Asked "What is the sum of 2 and 3?", it returns the call that would compute it:

```json
{
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {"a": 2.0, "b": 3.0}
}
```

The difficulty is that the model doing the work has 0.6 billion parameters. Asked for JSON, a model that size produces valid JSON perhaps 30% of the time, it will drop a brace or hallucinate.

The solution here is constrained decoding. The model emits one token at a time, chosen from a vocabulary of 151,936 options by picking the highest-scoring one.
At every position it computes which tokens could still lead to valid, schema-compliant output and makes every other token unreachable. The model only chooses from tokens that cannot break the format.

Two constrained passes produce each call.
The first walks a prefix tree of tokenized function names, so the model selects among the defined functions and cannot hallucinate one that does not exist. Once the name is known, so is its parameter schema, meaning the object's keys and punctuation can be written directly and the model is asked only to fill in values, each one constrained by a small state machine for its declared type.

The result is JSON that is valid by construction rather than by luck.

---

# Instructions

## Requirements
Python 3.10 or later and uv.

## Setup

```bash
uv sync
```

This creates the virtual environment and installs everything from `uv.lock`, including the bundled `llm_sdk` package. On the first run the Qwen3-0.6B weights (~1.2 GB) are downloaded and cached, so the first execution takes longer than subsequent ones.

## Running

```bash
uv run python -m src
```

By default this reads from `data/input/` and writes to `data/output/function_calling_results.json`. The output directory is created if it does not exist.

All three paths can be overridden:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

`uv run python -m src --help` lists the options.

## Make targets

| Target | What it does |
|---|---|
|`make install`| `uv sync` |
| `make run` | Run the pipeline on the default input files |
| `make debug` | Run it under `pdb` |
| `make lint` | `flake8 .` and `mypy .` with the required flags |
| `make lint-strict` | `flake8 .` and `mypy . --strict` |
| `make clean` | Remove caches and bytecode |
| `make fclean` | Remove output directory |

---

# Resources

## Documentation

- [Qwen3-0.6B model card](https://huggingface.co/Qwen/Qwen3-0.6B) --
  model details and chat template format.
- [Qwen3 chat template deep dive](https://huggingface.co/blog/qwen-3-chat-template-deep-dive)
  -- the `<|im_start|>` markers and how thinking mode is disabled.
- [Pydantic v2 documentation](https://docs.pydantic.dev/latest/concepts/models/)
  -- models, `TypeAdapter`, and validation errors.
- [uv documentation](https://docs.astral.sh/uv/) -- lockfile-based
  dependency management.
- [JSON specification](https://www.json.org/) -- the number and string
  grammars implemented in `grammar.py`.
- [Argparse documentation](https://docs.python.org/3/howto/argparse.html) -- the documentation for argparse.

## Use of AI

Claude by Anthropic was used in this project for the following:

- **As a teacher:** Explaining constrained decoding, byte-level BPE tokenization and how finite state machines apply to JSON grammar.
- **Design discussion:** Weighing the two-pass approach against a single whole-object grammar and where each module's responsibilities should sit.
- **Rewriting docstrings:** Improving clarity and precision of module and function-level documentation.
- **Testing:** Discussing edge cases and interpreting the results.


*AI was NOT used to write or generate any code. All function bodies were written by me.*

---

# Algorithm explanation

## Where the intervention happens

The SDK gives one method that hands a list of token IDs and gets back 151,936 raw scores, one per token in the vocabulary. Ordinary generation picks the highest and appends it. Constrained decoding inserts a step in between.

The subject describes this as setting invalid logits to negative infinity and taking the argmax of what remains. The implementation is equivalent but inverted, meaning that rather than modifying 151,936 floats and scanning them, it computes the set of legal tokens and takes the max over the set. After softmax the two are identical, a token with score `-inf` has a probability exactly zero and a token excluded from the set is equally unreachable.

## Two passes

This implementation avoids building one parser by splitting generation in two, exploiting the fact that after the first pass the schema is fully determined.

### Pass one: the function name

At startup every function name is tokenized and stored in a prefix tree keyed by token ID. Each node holds the token IDs that may follow it.

Generation reads the current node's children, masks to those, picks the best and advances. The loop ends when a node has no children, which happens only at a complete name.

### Pass two: the arguments

With the name known, the parameter names, their order and their types are all known from `functions_definition.json`. Everything structural can therefore be written rather than generated.

## The value grammars

Each type has a finite state machine walked one character at a time. Two questions have to be answered separately and conflating them is a mistake worth naming:

- **Is this a valid prefix?** Could the text still grow into something valid? `2.` can, so the decimal point must be allowed.
- **Is this complete?** Is it valid right now? `2.` is not, so generation must not stop there.

## From characters to tokens

The automata work on characters but the model emits tokens, and a single token can carry several characters. So a token is legal only if the whole text-so-far plus that token's text is still a valid prefix. The mask is built by testing every vocabulary entry against that condition.

## Stopping

Nothing in a value grammar says when to stop. `2` and `2000000` are both valid numbers. Termination is offered rather than forced: when the value is complete, the token for the separator that follows it is added to the allowed set. If the model picks it, the value is finished.

For strings the separator is merged with the closing quote. The tokenizer has single tokens for `",` and `"}`. Offering only the bare quote pushes generation onto a path the model may never take, so the merged tokens are what the grammar allows.

A constrained grammar guarantees validity but not termination: a model that keeps choosing legal digits stays inside valid output forever. Each value generator therefore has a hard token cap that turns a hang into a diagnosable error.

---

# Design decisions

## Prefill structure instead of generating it

Keys, colons, commas and braces are appended to the token sequence directly. They cost no forward pass and cannot come out wrong. The cost is that the grammar cannot see prefilled text: a missing quote after a key is invisible to the constraint and surfaces as strange model behaviour rather than a validation error.

## Restrict string content to printable ASCII

Byte-level BPE splits non-ASCII characters across tokens and a token carrying part of one decodes to the replacement character. That character is legal string content, so the model could emit it indefinitely.

## Validate once, at the boundary

Every file is parsed into pydantic models on load, so the rest of the program works with types that cannot be malformed. A file that is valid JSON but structurally wrong is rejected with a message naming the location.

---

# Performance analysis

| Machine | speed |
| --- | --- |
| personal machine | 38.6 seconds |
| campus machine | TODO |

A single forward pass costs 150-250 ms depending on machine load and the SDK exposes no key-value cache, so every step re-processes the whole sequence rather than extending it.

**Reliability.** Missing files, unreadable files, malformed JSON, valid JSON of the wrong shape and unknown parameter types all produce a single message and a non-zero exit code. Every generation loop is bounded so a model that will not terminate raises a diagnosable error.

---

# Challenges faced

## The prefill has to be exactly right and the grammar cannot tell you when it isn't

String values were coming out as ` \"Shrek`. I spent a long time in the string grammar looking for the bug only to find that the bug was the key prefix was being written as `"name: ` instead of `"name": `.

## Valid output does not mean generation ends

Asked for the sum of 2 and 3, the model produced 2, then 2., then 2.0, then zeros forever until the token cap fired. Every intermediate state was a valid JSON number so nothing in the grammar objected.
Then the model started emitting endlessly until at some point it abandoned the value entirely and began producing Chinese text. The output was still valid JSON the whole time.

Two fixes: printable ASCII only in string values and a hard token cap on every generation loop that turns a hang into an error naming the value being generated.

## The model would not close a string

Strings ran to the token limit on every prompt. The terminator was in the allowed set and the model kept declining it. The cause was that I offered a bare `"`, while the tokenizer has single tokens for `",` and `"}`. Offering only the bare quote pushed generation onto a path it would not take. Allowing the merged tokens fixed it immediately.
---

# Testing strategy

## Deliberately broken input files

A small set of malformed files, each targeting a different failure:
- truncated JSON, which fails during parsing;
- an empty file, which also fails during parsing but at a different position
- valid JSON of the wrong shape, which parses cleanly and fails validation

## End-to-end runs

The full pipeline is run against the provided example set and the results read directly. Because constrained decoding guarantees the output parses, the only interesting question is whether the values are right. Which no automated check can answer without expected answers to compare against.

## A second function catalogue

Running against a different catalogue is what exposed the real gaps: unsupported types failing late rather than at load, string values that needed escape sequences and the unbounded fractional digits.

---

# Example usage

## Default run

```bash
uv run python -m src
```

## Custom paths

```bash
uv run python -m src \
  --functions_definition path/to/functions_definition.json \
  --input path/to/prompts.json \
  --output path/to/results.json
```

## Error handling

Anticipated failures print one line to stderr and exit non-zero:
```bash
$ uv run python -m src --input missing.json ; echo "exit: $?"
Error: missing.json: file not found
exit: 1

$ uv run python -m src --input broken.json ; echo "exit: $?"
Error: broken.json: invalid JSON at line 2, column 1
exit: 1
```
