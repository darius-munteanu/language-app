import asyncio
import random

import edge_tts
from edge_tts import VoicesManager,Communicate
selected_gender = "Female"
async def _getvoice():
    """Main function"""
    voices = await VoicesManager.create()
    voice = voices.find(Gender=selected_gender, Language="es",Locale="es-ES")
    # Also supports Locales
    # voice = voices.find(Gender="Female", Locale="es-AR")
    return voice[0]["Name"]
#communicate = edge_tts.Communicate(TEXT, random.choice(voice)["Name"])
#await communicate.save(OUTPUT_FILE)

text = "Hola!! Como te llamas?"

OUTPUT_FILE = "media/test.mp3"

SPEECH_RATE = "+0%"  # Adjust the speech rate as needed
async def _main():
    tts = Communicate(
        text,
        VOICE,
        rate=SPEECH_RATE,
    )

    await Communicate.save(tts,OUTPUT_FILE)

x  = asyncio.run(_getvoice())
VOICE = x
print(x)
asyncio.run(_main())