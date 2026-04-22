import argparse
import re
import sys

SEPARATOR = "\n\n---\n"

parser = argparse.ArgumentParser()
parser.add_argument("--chat-file", required=True)
parser.add_argument("--speaker", required=True)
parser.add_argument("--starter", required=True)
parser.add_argument("--message-file")
parser.add_argument("--check-only", action="store_true")
args = parser.parse_args()

with open(args.chat_file, "r", encoding="utf-8") as f:
    content = f.read()

content = content.strip()

# Parse blocks
blocks = []
if content:
    parts = content.split(SEPARATOR)
    for p in parts:
        if not p.strip():
            continue
        lines = p.split("\n", 1)
        if len(lines) < 2 or not lines[0].endswith(":"):
            print("Invalid chat format", file=sys.stderr)
            sys.exit(2)
        speaker = lines[0][:-1]
        message = lines[1]
        blocks.append((speaker, message))

# Turn validation
if not blocks:
    if args.speaker != args.starter:
        sys.exit(3)
else:
    last_speaker = blocks[-1][0]
    if last_speaker == args.speaker:
        sys.exit(3)

if args.check_only:
    sys.exit(0)

if not args.message_file:
    print("Missing message file", file=sys.stderr)
    sys.exit(2)

with open(args.message_file, "r", encoding="utf-8") as f:
    message = f.read().strip()

if SEPARATOR.strip() in message:
    print("Message contains forbidden separator", file=sys.stderr)
    sys.exit(2)

block = f"{args.speaker}:\n{message}\n\n---\n"

if not content:
    new_content = block
else:
    new_content = content + SEPARATOR + block.replace(SEPARATOR, "")

with open(args.chat_file, "w", encoding="utf-8") as f:
    f.write(new_content)

sys.exit(0)
