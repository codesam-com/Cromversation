import argparse
import json
import sys

NAME_TO_EVENT = {
    "aurora": "aurora-turn",
    "boreal": "boreal-turn",
    "cyra": "cyra-turn",
}


def build_request(chat_file: str, model: str, output: str) -> None:
    with open(chat_file, "r", encoding="utf-8") as f:
        chat = f.read().strip()

    system_prompt = """
Eres el orquestador de una conversación entre tres personalidades: Aurora, Boreal y Cyra.

Tu función:
- leer el historial completo del chat
- decidir quién debe hablar a continuación
- no escribir nunca en el chat
- responder solo con uno de estos tres nombres exactos: Aurora, Boreal o Cyra

Criterios de decisión:
- usa el historial para mantener una conversación interesante, coherente y variada
- puedes repetir personalidad si tiene sentido, pero evita repeticiones mecánicas
- si una idea necesita profundidad, Aurora es buena opción
- si una idea necesita contraste o expansión, Boreal es buena opción
- si una idea necesita síntesis, aterrizaje o evaluación crítica, Cyra es buena opción
- no expliques tu decisión
- no añadas puntuación, JSON ni texto adicional
""".strip()

    user_prompt = f"""
Historial completo:
{chat if chat else '[vacío]'}

Devuelve solo el nombre exacto de la siguiente personalidad.
""".strip()

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
    }

    with open(output, "w", encoding="utf-8") as f:
        json.dump(payload, f)


def extract_event(response_file: str, output: str) -> None:
    with open(response_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    content = data["choices"][0]["message"]["content"].strip().lower()

    selected = None
    for name in NAME_TO_EVENT:
        if name in content:
            selected = name
            break

    if not selected:
        print("Could not map orchestrator response to a participant", file=sys.stderr)
        sys.exit(1)

    with open(output, "w", encoding="utf-8") as f:
        f.write(NAME_TO_EVENT[selected])


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True)

build_parser = subparsers.add_parser("build")
build_parser.add_argument("--chat-file", required=True)
build_parser.add_argument("--model", required=True)
build_parser.add_argument("--output", required=True)

extract_parser = subparsers.add_parser("extract")
extract_parser.add_argument("--response-file", required=True)
extract_parser.add_argument("--output", required=True)

args = parser.parse_args()

if args.command == "build":
    build_request(args.chat_file, args.model, args.output)
elif args.command == "extract":
    extract_event(args.response_file, args.output)
