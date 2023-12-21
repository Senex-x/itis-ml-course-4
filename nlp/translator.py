
from googletrans import Translator

translator = Translator()  # initalize the Translator object
translations = translator.translate(['see if this helps', 'tarun'], dest='hi')  # translate two phrases to Hindi
for translation in translations:  # print every translation
    print(translation.text)
