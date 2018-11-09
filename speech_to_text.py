
#Import the required module for text 
# to speech conversion 
from gtts import gTTS 
from os import startfile

# The text that you want to convert to audio 
print('The string')
mytext = input()
print('The number No.1')
mynum1 = str(input())
print('The number No.2')
mynum2 = str(input())
i = 1
mynum2s = []

while i < 10:
    mynum2s.append(mynum2)
    i += 1

myspeech = str(mynum1 + mytext + join(mynum2s, ','))

# Language in which you want to convert 
language = 'en'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed 
myobj = gTTS(text=myspeech, lang=language, slow=False) 

# Saving the converted audio in a mp3 file named 
# welcome 
myobj.save("welcome2.mp4") 
print('done')

startfile('welcome2.mp4')

# %%

language = 'en'

for text in ['a','b','c']:
    myobj = gTTS(text= text, lang=language, slow=False) 
    myobj.save(text + '.mp4')