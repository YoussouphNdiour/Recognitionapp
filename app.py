from flask import Flask, render_template, Response, request, redirect, url_for
from camera import Video
import sqlite3 as sql
import time

app = Flask(__name__)

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("select * from arriver ORDER BY temps_arrivee DESC LIMIT 5")
    rows = cur.fetchall()
    return render_template("list.html", rows=rows)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videoarriver')
def videoarriver():
    number_of_times = False
    while True:
        camera = Video()
        frame, predictions = camera.get_frame()
        seconds = time.time()
        local_time = str(time.ctime(seconds))
        if predictions != '':
            number_of_times = True
            print(number_of_times)
            rows = 1
            with sql.connect("database.db", timeout=100) as con:
                cur = con.cursor()
                cur.execute("SELECT COUNT(id) FROM arriver")
                cur_result = cur.fetchone()
                print(cur_result)
                row = cur_result[0]
                print(row)
                rows = rows + row
            con.close()
            with sql.connect("database.db", timeout=100) as con:
                temps_depart = "-"
                cur = con.cursor()
                cur.execute("INSERT INTO arriver (id, nom, temps_arrivee, temps_depart) VALUES (?,?,?,?);", (rows, predictions, local_time,temps_depart))
                con.commit()
            con.close()
            if number_of_times:
                return redirect(url_for('list', _external=True), )

@app.route('/videodepart')
def videodepart():
    number_of_times = False
    while True:
        camera = Video()
        frame, predictions = camera.get_frame()
        seconds = time.time()
        local_time = str(time.ctime(seconds))
        temps_depart = "-"
        if predictions != '':
            number_of_times = True
            print(number_of_times)
            with sql.connect("database.db", timeout=100) as con:
                cur = con.cursor()
                cur.execute("UPDATE arriver SET temps_depart = ? where nom=? AND temps_depart = ?;",(local_time, predictions, temps_depart))
                print(local_time, predictions, temps_depart)
                con.commit()
            con.close()
            if number_of_times:
                return redirect(url_for('list', _external=True), )

def gens(camera):
    while True:
        frame, predictions=camera.get_frame()
        yield(b'--frame\r\n' b'Content-Type:  image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/videos')
def videos():
    return Response(gens(Video()), mimetype='multipart/x-mixed-replace; boundary=frame')





if __name__ == '__main__':
    app.run(debug=True)
