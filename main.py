from flask_sqlalchemy import SQLAlchemy
import threading
from flask import Flask, render_template
import psutil
import time
from datetime import datetime
import  json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# создаем форму таблицы базы данных
class Cpuusage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)                                 # загрузка ЦП
    date = db.Column(db.DateTime, default=datetime.utcnow())    # дата/время внесения в БД

@app.route('/')
def index():
    values = [x.value for x in db.session.query(Cpuusage.value).distinct()]
    date1 = [x.date for x in db.session.query(Cpuusage.date).distinct()]
    data = json.dumps(time.mktime(date1[0].timetuple()) * 1000)
    return render_template('index.html', values=json.dumps(values), time=data)
def check_usage():
    """
    Собирает информацию о загрузке ЦП с заданным интервалом
    времени и вносит ее в БД. При завершении работы программы,
    БД очищается.
    """
    try:
        while True:
            usage = Cpuusage(value=psutil.cpu_percent(interval=1), date=datetime.now())
            db.session.add(usage)
            db.session.commit()
    except:
        db.session.rollback()
        print('Ошибка добавления в БД')
    finally:
        db.session.query(Cpuusage).delete()
        db.session.commit()

if __name__ == '__main__':
    # создаем отдельный поток для запуска сервера
    th = threading.Thread(target=app.run)
    th.start()
    # запускаем функцию сбора данных о загрузке ЦП
    check_usage()




