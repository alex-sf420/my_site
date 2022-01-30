from flask_sqlalchemy import SQLAlchemy
import threading
from flask import Flask, render_template
import psutil
import time
from datetime import datetime, timedelta
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
    """
    Отображает страницу html с переданной ей информацией о загрузке ЦП
    """
    now = datetime.now()
    info = db.session.query(Cpuusage.value, Cpuusage.date).filter(Cpuusage.date > (now - timedelta(hours=1))).all()
    value = [x[0] for x in info]
    print(len(value))
    date = [x[1] for x in info]
    print(len(date))
    time_for_js = [time.mktime(date[x].timetuple()) * 1000 for x in range(len(date))]
    return render_template('index.html', values=json.dumps(value), time=json.dumps(time_for_js))
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




