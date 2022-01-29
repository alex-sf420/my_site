from flask_sqlalchemy import SQLAlchemy
import threading
from flask import Flask, render_template
import psutil
from datetime import *
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
    # values = [1, 2, 3, 5, 6]
    time = [23, 24, 25, 26, 27]
    values = [x.value for x in db.session.query(Cpuusage.value).distinct()]
    # time = [x.date.time().replace(microsecond=0) for x in db.session.query(Cpuusage.date).distinct()]
    return render_template('index.html', values=json.dumps(values), time=json.dumps(time))

def check_usage():
    """
    Собирает информацию о загрузке ЦП с заданным интервалом
    времени и вносит ее в БД. При завершении работы программы,
    БД очищается.
    """
    try:
        while True:
            usage = Cpuusage(value=psutil.cpu_percent(interval=5), date=datetime.now())
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




