
#Import the required module for text 
# to speech conversion 
from gtts import gTTS 
from os import startfile


language = 'en'

for text in ['After alot of work....']:
    myobj = gTTS(text= text, lang=language, slow=False) 
    myobj.save(text + '.mp3')