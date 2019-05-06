from flask import Flask, request, g, jsonify
from flask import _app_ctx_stack
import pdb
app = Flask(__name__)
import sqlite3

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        conn = g._database = sqlite3.connect('kvstore.db')
        conn.execute('CREATE TABLE IF NOT EXISTS kvstore (key VARCHAR, value VARCHAR)')
        conn.commit()
    else:
      conn = g._database = sqlite3.connect('kvstore.db')
    return conn

@app.route("/put", methods=['POST'] )
def put_data():
    if request.method == "POST":
        fields = [k for k in request.form]
        if 'key' and 'value' in fields:
            values = [request.form[k] for k in request.form]
            data = dict(zip(fields, values))
            query="SELECT key, value FROM kvstore WHERE key='%s'" % data['key'] 
            cur=get_db().execute(query)
            kv=cur.fetchall()
            cur.close()

            if len(kv) == 1 and kv[0][0] == data['key'] and kv[0][1]== data['value']:
               return "Given key and value already exist \n"
            
            elif len(kv) == 1 and kv[0][0] == data['key'] and kv[0][1] != data['value']:
               query="UPDATE kvstore SET value='%s' WHERE key='%s'" % (data['value'],data['key'])
               cur= get_db()
               cur.execute(query)
               cur.commit()
               cur.close()
               return 'Given key already exist, updating the value \n'

            else:
               query="INSERT INTO kvstore(key,value) values ('%s','%s')" % (data['key'], data['value'])
               print(query)
               cur= get_db()
               cur.execute(query)
               cur.commit()
               cur.close()
               return 'Given key and value inserted \n'            
        
        else:
            return "incorrect key and value"

@app.route("/get", methods=['POST'] )
def get_data():
    if request.method == "POST":
        fields = [k for k in request.form]
        if 'key' in fields:
            values = [request.form[k] for k in request.form]
            data = dict(zip(fields, values))
            query="SELECT key, value FROM kvstore WHERE key='%s'" % data['key'] 
            cur=get_db().execute(query)
            kv=cur.fetchone()
            cur.close()

            if not kv:
               return "Given key Doesn't exist \n"
            else:
               key, value = kv[0], kv[1]
               return "key = %s \nvalue = %s \n" % (key,value)
        
        else:
               return "Given incorrect key "
    return "key value added successfully"



@app.route("/watch", methods=['GET'] )
def watch_data():
    if request.method == "GET":
        query = "SELECT * FROM kvstore"
        cur=get_db().execute(query)
        kv=cur.fetchall()
        cur.close()
        all_kv={}
                
        for i in kv:
            all_kv[i[0]]=str(i[1])
        return jsonify(all_kv)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
