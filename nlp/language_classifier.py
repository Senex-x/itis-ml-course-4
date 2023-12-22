# from pprint import pprint as print
# from gensim.models.fasttext import FastText
# from gensim.test.utils import datapath
import logging
import re


def get_wide_ordinal(char):
    if len(char) != 2:
        return ord(char)
    return 0x10000 + (ord(char[0]) - 0xD800) * 0x400 + (ord(char[1]) - 0xDC00)


def filter_text(text):
    filtered_text = []
    for letter in text:
        if letter == ' ' or letter in tatar_alphabet or letter in russian_alphabet:
            filtered_text.append(letter)
    return re.sub(' +', ' ', ''.join(filtered_text))


def filter_unique_only(source, other):
    unique_characters = []
    for letter in source:
        if letter not in other:
            unique_characters.append(letter)
    return unique_characters


message = 'Афиша Дома татарской книги на эту неделю / Татар китабы йортында бу атнада ниләр көтелә 💥  ▪️' \
          '5 сентябрь, 15:00. КАЛЛИГРАФИЯ Тылсымлы гарәп хәрефләре белән дуслашу мөмкинлеге. ' \
          '⏺Возможность подружиться с волшебной арабской вязью.   ' \
          '▪️6 сентябрь 14:00. ӘДӘБИ ОСТАХАНӘ «Яңа исем» лабораториясендә Лилия Гыйбадуллинадан шигърият дәресе ' \
          '⏺Мастер-класс по поэзии от Лилии Гибадуллиной. В рамках лаборатории «Яна исем»  ' \
          '▪️6 сентябрь, 16:00. BEATMAKING. ABLETON LIVE 11 Бергәләп Ableton Live кушымтасында музыка иҗат итү нигезләрен өйрәнәбез. ' \
          '⏺Возможность научиться творчеству в программе Ableton Live. ' \
          ' ▪️6 сентябрь, 18:00. ЧЕРДАЧНЫЕ ИСТОРИИ Татарларда булган хорафатлар һәм ышанулар турында квест узып, Йортның чормасында сакланган серләрне чишә алырсыз. ' \
          '⏺Возможность узнать о поверьях и суевериях татар, пройти квест и заглянуть в чердак Дома татарской книги.  ' \
          '▪️7 сентябрь, 15:00. ЧӘЙ Татар әдәбенә туры китереп чәй эчәргә өйрәнәбез. ⏺Учимся чаепитию согласно татарскому этикету.  ' \
          '▪️8 сентябрь, 18:00. СОБРАНИЕ КНИЖНОГО КЛУБА ЛОГОС Клубның туган көне! ⏺На традиционном «книжном собрании» отметят День рождение клуба!  ' \
          '▪️8 сентябрь 16:00. BEATMAKING. ABLETON LIVE 11 Бергәләп Ableton Live кушымтасында музыка иҗат итү нигезләрен өйрәнәбез. ' \
          '⏺Возможность научиться творчеству в программе Ableton Live.  ' \
          '▪️8 сентябрь, 17:30. ЧЕРДАЧНЫЕ ИСТОРИИ Татарларда булган хорафатлар һәм ышанулар турында квест узып, Йортның чормасында сакланган серләрне чишә алырсыз. ' \
          '⏺Возможность узнать о поверьях и суевериях татар, пройти квест и заглянуть в чердак Дома татарской книги.  ' \
          '▪️9 сентябрь, 18:00. «ТЫЛСЫМЛЫ УКУ» Һарри Поттерны татарча да укып булганын беләсездер инде. Әмма аны бергәләп уку тагын да күңеллерәк һәм… тылсымлырак! Ә аннары квиз үтәрбез! ' \
          '⏺ Читаем Гарри Поттера на татарском вместе!  ▪️10 сентябрь, 13:00. ЭКСКУРСИЯ Татарларда китапчылык тарихы турында беләсегез килсә, рәхим итегез ' \
          '⏺ Обзорная экскурсия «История книги от пергамента до цифры»  📍Казань, ул. Островского, д. 15 ☎️ (843) 590-80-66,  (843) 590-80-67'

tatar_alphabet = 'А а Ә ә Б б В в Г г Д д Е е Ё ё Ж ж Җ җ З з И и Й й К к Л л М м Н н Ң ң О о Ө ө П п Р р С с Т т У у Ү ү Ф ф Х х Һ һ Ц ц Ч ч Ш ш Щ щ Ъ ъ Ы ы Ь ь Э э Ю ю Я я'.split()

russian_alphabet = 'А а Б б В в Г г Д д Е е Ё ё Ж ж З з И и Й й К к Л л М м Н н О о П п Р р С с Т т У у Ф ф Х х Ц ц Ч ч Ш ш Щ щ Ъ ъ Ы ы Ь ь Э э Ю ю Я я'.split()

unique_tatar_alphabet = ['Ә', 'ә', 'Җ', 'җ', 'Ң', 'ң', 'Ө', 'ө', 'Ү', 'ү', 'Һ', 'һ']

import re
import codecs

# import fasttext
#
# PRETRAINED_MODEL_PATH = '/tmp/lid.176.bin'
# model = fasttext.load_model(PRETRAINED_MODEL_PATH)

import csv

COLUMNS = [
    "msg_id",
    "date",
    "msg_content",
]

COLUMNS2 = [
    "date",
    "msg_content",
]

tatar_file = codecs.open('tatar_messages.csv', 'w', "utf_8_sig")
uncertain_file = codecs.open('uncertain_messages.csv', 'w', "utf_8_sig")
certain_file = codecs.open('certain.csv', 'w', "utf_8_sig")

csv_writer = csv.DictWriter(tatar_file, COLUMNS, dialect="unix", quoting=csv.QUOTE_NONNUMERIC)
csv_writer.writeheader()

csv_writer_uncertain = csv.DictWriter(uncertain_file, COLUMNS, dialect="unix", quoting=csv.QUOTE_NONNUMERIC)
csv_writer_uncertain.writeheader()

csv_writer_certain = csv.DictWriter(certain_file, COLUMNS2, dialect="unix", quoting=csv.QUOTE_NONNUMERIC)

csv_writer_leftover = csv.DictWriter(codecs.open('tatar_leftover_messages.csv', 'w', "utf_8_sig"), COLUMNS, dialect="unix", quoting=csv.QUOTE_NONNUMERIC)

with open('original_messages.csv', encoding="utf-8-sig", ) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        id = row[0]
        date = row[1]
        message = row[2]

        classified = False

        for tatar_letter in unique_tatar_alphabet:
            if tatar_letter in message:
                csv_writer.writerow({
                    "msg_id": id,
                    "date": date,
                    "msg_content": message,
                })
                classified = True
                break

        if not classified:
            csv_writer_uncertain.writerow({
                "msg_id": id,
                "date": date,
                "msg_content": message,
            })


trigger_ru_words = 'домтатарскойкниги музейонлайн Афиша приглашаем Спикер: Регистрация'.split()

import re

with open('tatar_messages.csv', encoding="utf-8-sig", ) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        id = row[0]
        date = row[1]
        message = row[2]

        classified = False

        for word in trigger_ru_words:
            if re.search(word, message, re.IGNORECASE):
                csv_writer_certain.writerow({
                    "date": date,
                    "msg_content": message,
                })
                classified = True
                break

        if not classified:
            csv_writer_leftover.writerow({
                "msg_id": id,
                "date": date,
                "msg_content": message,
            })

# import polyglot
# from polyglot.text import Text, Word
# text = Text("Bonjour, Mesdames.")
# text.language

# DOESN'T WORK
# from langdetect import detect_langs, DetectorFactory
# DetectorFactory.seed = 0
# print(detect_langs('Татар китабы йортында бу атнада ниләр көтелә'))


# import cld3
# cld3.get_language("影響包含對氣候的變化以及自然資源的枯竭程度")
# LanguagePrediction(language='zh', probability=0.999969482421875, is_reliable=True, proportion=1.0)


# fileObj = codecs.open("text.txt", "r", "utf_8_sig")
# text = fileObj.read()  # или читайте по строке
# text = re.sub('0...', '', text)
# text = text.replace("\n", " ").replace("\r", "").replace("  ", " ")
# print(len(text))
# print(text)
# fileObj.close()
#
# codecs.open('out.txt', 'w', "utf_8_sig").write(text)


# print('tat')
# for letter in tatar_alphabet:
#     print(get_wide_ordinal(letter[0]))
# print('ru')
# for letter in russian_alphabet:
#     print(get_wide_ordinal(letter[0]))
