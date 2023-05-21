#!/usr/bin/env python3
import sys
import queue
import sounddevice as sd
import vosk as talk
import json
from sklearn.feature_extraction.text import CountVectorizer    
from sklearn.linear_model import LogisticRegression
from modules.experience import *
import voice

# глобально отключаем ванринги
import warnings 
warnings.filterwarnings("ignore")


q = queue.Queue()

# отключаем логи vosk
talk.SetLogLevel(-1)
model_ru = talk.Model('model_small_ru')


device = sd.default.device     
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  
#[1, 3]
#44100



def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize(data, vectorizer, clf):
    #читаем файл triggers.yaml
    trigger = load_file('configs/triggers.yaml')
    
    #проверяем есть ли имя бота в data, если нет, то return
    trg = [ string for string in trigger['TRIGGERS'] if  string in data]
    if not trg:
        return
    

    #удаляем имя бота из текста
    query = data.replace(list(trg)[0], '')

    #получаем вектор полученного текста
    #сравниваем с вариантами, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    print(answer)


    #получение имени функции из ответа из words
    func_name = answer.split()[0]

    #озвучка ответа из модели words
    voice.speaker(answer.replace(func_name, ''))

    #запуск функции из skills
    exec(func_name + '(query)')
    
    


def main():
    # читаем файл dictonary.yaml
    words = load_file('configs/dictonary.yaml')

    #Обучение матрицы на words модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.keys()))
    
    clf = LogisticRegression()
    clf.fit(vectors, list(words.values()))

    del words

    with sd.RawInputStream(samplerate=samplerate, 
                        blocksize = 44100, device=device,
                        dtype="int16", channels=1, callback=callback):

        rec_ru = talk.KaldiRecognizer(model_ru, samplerate)
        
        while True:
            data = q.get()
            if rec_ru.AcceptWaveform(data):
                data = json.loads(rec_ru.Result())['text']
                recognize(data, vectorizer, clf)
                print(data)
            
if __name__=='__main__':
    try:  
        main()
    except KeyboardInterrupt:
        print('До побачення!')
        sys.exit()                
            

