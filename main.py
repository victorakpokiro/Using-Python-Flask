
from flask import (Flask, render_template, 
                    redirect, url_for, abort,
                    send_from_directory, request
                    )

import os 

from model import db_conn_mgr, create_table

import datetime 


app = Flask(__name__)
app.config.update({'DEBUG': True, 'ENV': 'development'})


@app.route("/styles/<path:filename>")
def custom_files(filename):

    _type = 'text/javascript'
    if filename.endswith('.css'):
        _type = 'text/css'
    
    return send_from_directory(
            'static/', 
            filename, mimetype=_type, 
            )
 



@app.route('/')
def index():
    
    qry = []

    with db_conn_mgr() as db:
        resp = db.query("""select 
                            id, title, status, filename, 
                            date_created 
                            from blogtbl order by id desc limit 10
                        """)

        qry = resp.all()



    return render_template('view.html', data=qry)


@app.route('/article/add', methods=['POST', 'GET'])
def add_article():

    if request.method == 'POST':
        
        _file = request.files['_filecontent']
        _path = os.path.join('static/blgpix', _file.filename)
        _file.save(_path)
        
        params = {
            'title': request.form['_title'],
            'status': request.form['blog_status'],
            'filename': _path,
            'date_created': datetime.datetime.now()
        }

        with db_conn_mgr() as db:
            
            resp = db.query("""select id from blogtbl  order by id desc 
                                limit 1 
                            """)

            output = resp.all()

            if output: 
                next_id = output[0].id + 1 

            else:
                next_id = 1 

            params['id'] = next_id

            db.query('''
                insert into blogtbl 
                values ( 
                    :id, :title, :status, :filename, :date_created
                )
            ''', **params)



            return redirect('/')

 
    return render_template('add.html')






# --------------------------+-----------------------------+
# --------------------------+-----------------------------+

if __name__ == '__main__':
    
    fl = open('blogtbl.SQL', 'r')
    create_table(fl.read())
    fl.close()

    app.run(port=5050)

