from flask_sqlalchemy import SQLAlchemy
import threading
from flask import Flask, render_template
import psutil
import time
from datetime import datetime, timedelta
import  json
from statistics import mean

INTERVAL = 1 # константа, определяющая интервал записи в БД в сек.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# создаем форму таблицы базы данных
class Cpuusage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)                                 # загрузка ЦП
    date = db.Column(db.DateTime, default=datetime.utcnow())    # дата/время внесения в БД

def make_empty_lists(info):
    """
    Принамает список базы данных. Возвращает список пустых списков,
    соответствующих количеству минут
    """
    return [[] for x in range(len(info) // (5//INTERVAL))] # по количеству минут

def calculates_the_average_value(array):
    """
    Принимает двумерный список. Возвращает список средних значений
    """
    return [round(mean(x), 1) for x in array]

@app.route('/')
def index():
    """
    Получает из БД данные value и date за заданный отрезок времени с последующей
    сериализацией данных.
    Рассчитывает средние значения данных value и date.
    Отображает страницу html с переданной ей информацией о загрузке ЦП
    """
    now = datetime.now()
    # получаем значения базы данных по столбцам value и date
    # за указанный период
    info = db.session.query(Cpuusage.value, Cpuusage.date).filter(Cpuusage.date >\
                                                                  (now - timedelta(hours=1))).all()
    # формируем отдельные списки данных для первого графика
    value = [x[0] for x in info]
    date = [x[1] for x in info]
    # создаем пустые списки для второго графика
    average_value = make_empty_lists(info)
    average_date = make_empty_lists(info)
    # заполняем сведения для второго графика двумерными списками
    counter = 0 # счетчик для сплошного обхода списков
    for i in range(len(info) // (5//INTERVAL)): # количество циклов по количеству минут
        for j in range(5 // INTERVAL): # количество записей в БД в минуту
            average_value[i].append(value[counter])
            # переводим в Unix time, умножая на 1000 для корректного чтения в js
            average_date[i].append(time.mktime(date[counter].timetuple()) * 1000)
            counter += 1
    else:
        # считаем среднее значение за 1 мин для второго графика
        average_value = calculates_the_average_value(average_value)
        average_time_for_js = calculates_the_average_value(average_date)
    # переводим в Unix time список для первого графика
    time_for_js = [time.mktime(date[x].timetuple()) * 1000 for x in range(len(date))]
    return render_template('index.html', values=json.dumps(value), time=json.dumps(time_for_js),\
                           average_value=json.dumps(average_value), \
                           average_time=json.dumps(average_time_for_js), interval=json.dumps(INTERVAL*1000))
def check_usage():
    """
    Собирает информацию о загрузке ЦП с заданным интервалом
    времени и вносит ее в БД. При завершении работы программы,
    БД очищается.
    """
    try:
        while True:
            usage = Cpuusage(value=psutil.cpu_percent(interval=INTERVAL), date=datetime.now())
            db.session.add(usage)
            db.session.commit()
    except:
        db.session.rollback()
        print('Ошибка добавления в БД')

if __name__ == '__main__':
    # создаем отдельный поток для запуска сервера
    th = threading.Thread(target=app.run)
    th.start()
    # запускаем функцию сбора данных о загрузке ЦП
    check_usage()