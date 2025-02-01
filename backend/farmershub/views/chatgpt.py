import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from openai import OpenAI

logger = logging.getLogger(__name__)

# OpenAI-Client initialisieren
client = OpenAI(api_key=settings.OPENAI_API_KEY)


@csrf_exempt
def chat_with_gpt(request):
    """
    API-Endpunkt für die Kommunikation mit OpenAI GPT.
    """
    if request.method == "POST":
        try:
            # Anfrage-Daten parsen
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                logger.error("Nachricht fehlt")
                return JsonResponse({"error": "Nachricht fehlt"}, status=400)

            # Anfrage an OpenAI senden
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Bitte antworte immer auf Deutsch."},
                    {"role": "user", "content": user_message}
                ]
            )

            # Antwort extrahieren
            gpt_reply = response.choices[0].message.content
            return JsonResponse({"reply": gpt_reply}, status=200)

        except Exception as e:
            logger.exception("Fehler in der Funktion chat_with_gpt:")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)
