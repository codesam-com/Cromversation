import argparse
import sys

BLOCK_SEPARATOR = "\n\n---\n\n"
FINAL_SUFFIX = "\n\n---\n"


def parse_blocks(raw: str):
    text = raw.strip()
    if not text:
        return []

    normalized = text
    while "\n\n---\n\n---\n" in normalized:
        normalized = normalized.replace("\n\n---\n\n---\n", "\n\n---\n\n")
    normalized = normalized.removesuffix("\n")
    normalized = normalized.removesuffix("---")
    normalized = normalized.rstrip()

    parts = normalized.split(BLOCK_SEPARATOR)
    blocks = []
    for part in parts:
        chunk = part.strip()
        if not chunk:
            continue
        lines = chunk.split("\n", 1)
        if len(lines) != 2 or not lines[0].endswith(":"):
            print("Invalid chat format", file=sys.stderr)
            sys.exit(2)
        speaker = lines[0][:-1]
        message = lines[1].strip()
        blocks.append((speaker, message))
    return blocks


parser = argparse.ArgumentParser()
parser.add_argument("--chat-file", required=True)
parser.add_argument("--speaker", required=True)
parser.add_argument("--starter", required=False)
parser.add_argument("--message-file")
parser.add_argument("--check-only", action="store_true")
args = parser.parse_args()

with open(args.chat_file, "r", encoding="utf-8") as f:
    original = f.read()

blocks = parse_blocks(original)

if args.check_only:
    sys.exit(0)

if not args.message_file:
    print("Missing message file", file=sys.stderr)
    sys.exit(2)

with open(args.message_file, "r", encoding="utf-8") as f:
    message = f.read().strip()

if not message:
    print("Empty message", file=sys.stderr)
    sys.exit(2)

if "\n\n---\n" in message:
    print("Message contains forbidden separator", file=sys.stderr)
    sys.exit(2)

blocks.append((args.speaker, message))
rendered = BLOCK_SEPARATOR.join(f"{speaker}:\n{message}" for speaker, message in blocks) + FINAL_SUFFIX

with open(args.chat_file, "w", encoding="utf-8") as f:
    f.write(rendered)
