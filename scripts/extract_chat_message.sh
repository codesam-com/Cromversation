#!/bin/bash
set -euo pipefail

response_file="$1"
output_file="$2"
speaker="$3"

if jq -e '.choices[0].message.content | type == "string"' "$response_file" >/dev/null 2>&1; then
  jq -r '.choices[0].message.content' "$response_file" > "$output_file"
  exit 0
fi

case "$speaker" in
  Aurora)
    fallback="Retomo el hilo desde una pregunta sencilla: ¿qué aspecto de lo que se ha dicho merece profundizarse ahora mismo?" ;;
  Boreal)
    fallback="Voy a abrir una nueva arista: quizá aún no hemos mirado esta idea desde su lado más ambiguo o inesperado." ;;
  Cyra)
    fallback="Haré una síntesis breve para no perder el rumbo: conviene fijar la idea central antes de seguir expandiéndola." ;;
  *)
    fallback="Sigo la conversación desde el punto actual, intentando aportar continuidad y claridad." ;;
esac

printf '%s' "$fallback" > "$output_file"
