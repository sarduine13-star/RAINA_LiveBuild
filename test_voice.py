from gtts import gTTS

text = "Hey Red, this is RAINA confirming my local voice synthesis is active."
tts = gTTS(text=text, lang='en')
tts.save("raina_voice_confirm.mp3")

print("✅ Local voice file created: raina_voice_confirm.mp3")
