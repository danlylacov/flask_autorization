from flask import Flask, request, render_template, Response
import sqlite3
from camera import VideoCamera

app = Flask(__name__)


@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute(('''SELECT password FROM passwords
                                               WHERE login = '{}';
                                               ''').format(Login))
        pas = cursor_db.fetchall()
        print(pas)
        cursor_db.close()
        try:
            if pas[0][0] != Password:
                return render_template('auth_bad.html')
        except:
            return render_template('auth_bad.html')

        db_lp.close()
        return render_template('successfulauth.html')

    return render_template('authorization.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        try:
            sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(Login, Password)
            cursor_db.execute(sql_insert)
        except:
            return render_template('badregis.html')

        cursor_db.close()

        db_lp.commit()
        db_lp.close()

        return render_template('successfulregis.html')

    return render_template('registration.html')


@app.route('/registration/face', methods=['GET', 'POST'])
def form_face():
    return render_template('face.html')


def gen(camera):
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/registration/face/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
