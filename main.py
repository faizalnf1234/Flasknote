from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_mysqldb import MySQL,MySQLdb

app = Flask(__name__)

# Change this to your secret key, use https://passwordsgenerator.net/ for auto generate
app.secret_key = 'QgH7r?wD?Pz@UsC&'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flasknoter44_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Intialize MySQL
mysql = MySQL(app)

#### App Route ####
@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')
    
@app.route('/searchnote')
def searchnote():
    query = request.args.get('q')
    return render_template('searchnote.html',query=query)

@app.route('/addnote',methods=['GET','POST'])
def addnote():
    return render_template('addnote.html')

@app.route('/viewnote/<id>',methods=['GET'])
def viewnote(id):
    id_note = id
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM mynotes44 WHERE id_note=%s',(id_note,))
        data = cur.fetchone()
        return render_template('viewnote.html',data=data)
    except Exception as e:
        print(e)
    finally:
        cur.close()

@app.route('/editnote/<id>', methods=['GET','POST'])
def editnote(id):
    id_note = id
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM mynotes44 WHERE id_note=%s',(id_note,))
        data = cur.fetchone()
        return render_template('editnote.html',data=data)
    except Exception as e:
        print(e)
    finally:
        cur.close()

@app.route('/deletenote/<id>', methods=['GET'])
def deletenote(id):
    id_note = id
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('DELETE FROM mynotes44 WHERE id_note=%s',(id_note,))
        mysql.connection.commit()
        return render_template('viewnote.html')
    except Exception as e:
        print(e)
    finally:
        cur.close()

#### AJAX route ####
@app.route('/ajax/fetchnote', methods=['GET'])
def ajaxfetchnote():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM mynotes44')
        data = cur.fetchall()
        return jsonify(data)
    except Exception as e:
        print(e)
    finally:
        cur.close()

@app.route('/ajax/insertnote', methods=['POST'])
def ajaxinsertnote():
    if request.method == 'POST':
        data = request.get_json()
        try:
            title =  data['title']
            note = data['note']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('INSERT INTO mynotes44 (title_note,html_note) VALUES (%s,%s)',(title,note))
            mysql.connection.commit()
            msg = {
                'msg':'Note Created Successfully'
            }
            return jsonify(msg)
        except Exception as e:
            print(e)
        finally:
            cur.close()
    else:
        msg = {
            'msg':'Some error in request data'
        }
        return jsonify(msg)

@app.route('/ajax/updatenote', methods=['POST'])
def ajaxupdatenote():
    if request.method == 'POST':
        data = request.get_json()
        try:
            id = data['id']
            title =  data['title']
            note = data['note']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('UPDATE mynotes44 SET title_note=%s, html_note=%s WHERE id_note=%s',(title,note,id))
            mysql.connection.commit()
            msg = {
                'msg':'Note Edited Successfully'
            }
            return jsonify(msg)
        except Exception as e:
            print(e)
        finally:
            cur.close()
    else:
        msg = {
            'msg':'Some error in request data'
        }
        return jsonify(msg)

@app.route('/ajax/findnote', methods=['POST'])
def ajaxfindnote():
    if request.method == 'POST':
        data = request.get_json()
        try:
            query = data['query']
            q = '%'+query+'%'
            q2 = q
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cur.execute("SELECT * FROM mynotes44 WHERE title_note LIKE %s",(q,))
            cur.execute("SELECT * FROM mynotes44 WHERE title_note LIKE %s OR html_note LIKE %s",(q,q2))
            data = cur.fetchall()
            return jsonify(data)
        except Exception as e:
            print(e)
        finally:
            cur.close()
    else:
        msg = {
            'msg':'Some error in request data'
        }
        return jsonify(msg)

if __name__ == '__main__':
    app.run(debug=True)
