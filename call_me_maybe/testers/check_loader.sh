#!/usr/bin/env bash
# Exercises the CLI + loader against normal and malformed inputs.
# Run from the project root:  bash check_loader.sh
 
echo "=== 1. normal run (expect: two counts, exit 0) ==="
cd ..
uv run python -m src ; echo "exit: $?"
echo
 
echo "=== 2. truncated JSON (expect: clean error, exit 1) ==="
uv run python -m src --input data/test/truncated.json ; echo "exit: $?"
echo
 
echo "=== 3. empty file (expect: clean error, exit 1) ==="
uv run python -m src --input data/test/empty.json ; echo "exit: $?"
echo
 
echo "=== 4. valid JSON, wrong shape (expect: clean error, exit 1) ==="
uv run python -m src --input data/test/wrong_shape.json ; echo "exit: $?"
echo
 
echo "=== 5. missing file (expect: clean error, exit 1) ==="
uv run python -m src --input data/test/nope.json ; echo "exit: $?"
echo
 
echo "=== 6. same checks on the functions file ==="
uv run python -m src --functions_definition data/test/wrong_shape.json ; echo "exit: $?"
uv run python -m src --functions_definition data/test/nope.json ; echo "exit: $?"
echo
 
echo "=== 7. a directory instead of a file (expect: clean error, exit 1) ==="
uv run python -m src --input data/input ; echo "exit: $?"
echo
 
echo "=== 8. help screen ==="
uv run python -m src --help
echo
 
echo "=== 9. lint ==="
make lint
