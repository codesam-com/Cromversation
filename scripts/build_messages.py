import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--persona-file", required=True)
parser.add_argument("--chat-file", required=True)
parser.add_argument("--speaker", required=True)
parser.add_argument("--other-speaker", required=True)
parser.add_argument("--model", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

with open(args.persona_file, "r", encoding="utf-8") as f:
    persona = f.read()

with open(args.chat_file, "r", encoding="utf-8") as f:
    chat = f.read()

system_prompt = f"""
Eres {args.speaker}.

Instrucciones de personalidad:
{persona}

Reglas estrictas:
- Lee todo el historial antes de responder
- Responde solo con el mensaje, sin incluir el nombre de la personalidad
- No incluyas separadores como ---
- No uses bloques de código
- Mantén coherencia con el historial
- Prefiere ser conciso pero sin límite estricto
"""

user_prompt = f"""
Historial de conversación:
{chat if chat.strip() else '[vacío]'}

Escribe el siguiente mensaje de {args.speaker}. El otro participante es {args.other_speaker}.
"""

payload = {
    "model": args.model,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
}

with open(args.output, "w", encoding="utf-8") as f:
    json.dump(payload, f)
