import librosa as lr
import numpy as np
import psycopg2 as db
SR = 16000 # Частота дискретизации

def process_audio(aname):
  audio, _ = lr.load(aname, sr=SR) # Загружаем трек в память

  # Извлекаем коэффициенты
  afs = lr.feature.mfcc(audio, # из нашего звука
                        sr=SR, # с частотой дискретизации 16 кГц
                        n_mfcc=34, # Извлекаем 34 параметра
                        n_fft=2048) # Используем блоки в 125 мс
  # Суммируем все коэффициенты по времени
  # Отбрасываем два первых, так как они не слышны человеку и содержат шум
  afss = np.sum(afs[2:], axis=-1)

  # Нормализуем их
  afss = afss / np.max(np.abs(afss))

  return afss

def confidence(x, y):
  return np.sum((x - y)**2) # Евклидово расстояние
  # Меньше — лучше


def voice_identify(file_name):
  # Задаем настройки базы данных и подлючаемся к ней
  con = db.connect(
    database="voice_recognition_data", 
    user="postgres", 
    password="spongebob", 
    host="127.0.0.1", 
    port="5432"
  )

  audio = process_audio(file_name)

  cur = con.cursor()

  cur.execute("SELECT wav_data FROM men ") # Извлекаем из таблицы с мужскими аудио столбец с массивами значений MFCC
  paths= cur.fetchall()

  man_sum = 0
  man_count = 0
  men_audio = []
  # Получаем массив коэффициентов всех мужских файлов
  for i in range(len(paths)):
    temp_arr = []
    for j in range(len(paths[i][0])):
        temp_arr.append(float(paths[i][0][j]))
    men_audio.append(temp_arr)
  for man_audio in men_audio:
     # Получаем массив коэффициентов одного файла
     man_sum += confidence(man_audio, audio) # Суммируем все коэффициенты MFCC файла из БД и заданного файла
     man_count += 1 # Считаем количество аудиозаписей мужского пола

  cur.execute("SELECT wav_data FROM women ") # Извлекаем из таблицы с женскими аудио столбец с массивами значений MFCC
  paths= cur.fetchall()

  woman_sum = 0
  woman_count = 0
  women_audio = []
  # Получаем массив коэффициентов всех женских файлов
  for i in range(len(paths)):
    temp_arr = []
    for j in range(len(paths[i][0])):
        temp_arr.append(float(paths[i][0][j]))
    women_audio.append(temp_arr)
  for woman_audio in women_audio:
     # Получаем массив коэффициентов одного файла
     woman_sum += confidence(woman_audio, audio) # Суммируем все коэффициенты MFCC файла из БД и заданного файла
     woman_count += 1 # Считаем количество аудиозаписей мужского пола
  
  username = "" 
  username_rate = 100
  # Сравниваем среднее значение MFCC
  if man_sum/man_count < woman_sum/woman_count: # Если заданный файл от мужского пользователя
    cur.execute("SELECT name FROM men ") # Извлекаем из таблицы имена мужских пользователей
    paths= cur.fetchall()
    for i in range(len(men_audio)):
      audio_for_compare = men_audio[i] # Получаем массив коэффициентов одного файла
      if confidence(audio_for_compare, audio) < 1 and confidence(audio_for_compare, audio) <= username_rate: # Если выбранный файл из БД близок с заданным
        username_rate = confidence(audio_for_compare, audio) # Считаем MFCC
        username =  paths[i][0]# Присваеваем имя пользовcателю
    if username_rate != 100: # Если найден файл схожий с заданным
      return "Man", username
    else:
      return "Man", "We cann't identify you" # Если не найден файл схожий с заданным
  else:
    # Если заданный файл от женского пользователя
    cur.execute("SELECT name FROM women ") # Извлекаем из таблицы имена женских пользователей
    paths= cur.fetchall()
    for i in range(len(women_audio)):
      audio_for_compare = women_audio[i] # Получаем массив коэффициентов одного файла
      if confidence(audio_for_compare, audio) < 1 and confidence(audio_for_compare, audio) <= username_rate: # Если выбранный файл из БД близок с заданным
        username_rate = confidence(audio_for_compare, audio) # Считаем MFCC
        username =  paths[i][0]# Присваеваем имя пользовcателю
    if username_rate != 100: # Если найден файл схожий с заданным
      return "Woman", username
    else: # Если не найдем файл схожий с заданным
      return "Woman", "We cann't identify you"

  con.close()

def user_insert(file_name, name, sex):
  # Задаем параметры базы данных и подлючаемся к ней
  con = db.connect(
    database="voice_recognition_data", 
    user="postgres", 
    password="spongebob", 
    host="127.0.0.1", 
    port="5432"
  )

  cur = con.cursor()

  user = process_audio(file_name) # Получаем коэффициенты MFCC аудио файла
  user_float = []
  if sex.lower() == "man": # Если пользователь мужского пола
    for i in range(len(user)):
      user_float.append(float(user[i])) # Преобразуем коэффициенты в float
    cur.execute("INSERT INTO men (name, wav_data) VALUES (%s,%s)",(name,(user_float,))) # Добавляем в базу данных
  elif sex.lower() == "woman": # Еслм пользователь женского пола
    for i in range(len(user)):
      user_float.append(float(user[i])) # Преобразуем коэффициенты в float
    cur.execute("INSERT INTO women (name, wav_data) VALUES (%s,%s)",(name,(user_float,))) # Добавляем в базу данныхё

  con.commit()          
  con.close()

def printF():
  print("Work")
