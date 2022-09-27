from flask import Flask, render_template,request,redirect,url_for
import pymysql
db_connection = None
tb_cursor = None

app=Flask(__name__)

@app.route("/")
def index():
    detailsData = getAllDetails()
    return render_template("index.html",data=detailsData)

@app.route("/add/",methods=["GET","POST"])
def addDetail():
    if request.method=="POST":
        data = request.form
        isInserted = insertIntoTable(data['txtName'],data['txtAge'],data['txtGender'],data['txtContact'])
        if(isInserted):
            message = "Insertion sucess"
            return redirect(url_for("index")) 
        else:
            message = "Insertion error"
            return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/update/",methods=["GET","POST"])
def updateDetail():
    id = request.args.get("ID",type=int,default=1)
    idData = getDetailID(id)
    if request.method == "POST":
        data = request.form
        print(data)
        isUpdated = updateDetailIntoTable(data['txtName'],data['txtAge'],data['txtGender'],data['txtContact'],id)
        if(isUpdated):
            message = "Updattion sucess"
            return redirect(url_for("index"))
        else:
            message = "Updattion Error"
        return redirect(url_for("index"))
    return render_template("update.html",data=idData)


@app.route("/delete/")
def deleteDetail():
    id = request.args.get("ID",type=int,default=1)
    deleteDetailFromTable(id)
    return redirect(url_for("index"))

def dbConnect():
    global db_connection, tb_cursor
    db_connection=pymysql.connect(host="localhost",
    user="root",passwd="",database="gms",port=3306)
    if(db_connection):
        print("Connected")
        tb_cursor = db_connection.cursor()
    else:
        print("Not Connected")

def dbDisconnect():
    db_connection.close()
    tb_cursor.close()

def getAllDetails():
    dbConnect()
    getQuery="select * from details"
    tb_cursor.execute(getQuery)
    detailsData = tb_cursor.fetchall()
    dbDisconnect()
    return detailsData

def insertIntoTable(name,age,gender,contact):
    dbConnect()
    insertQuery = "INSERT INTO Details(name,age,gender,contact) VALUES(%s, %s, %s, %s);"
    tb_cursor.execute(insertQuery,(name,age,gender,contact))
    db_connection.commit()
    dbDisconnect()
    return True

def getDetailID(detail_id):
    dbConnect()
    selectQuery = "SELECT * FROM details WHERE ID=%s;"
    tb_cursor.execute(selectQuery,(detail_id,))
    oneData = tb_cursor.fetchone()
    dbDisconnect()
    return oneData

def updateDetailIntoTable(name,age,gender,contact,id):
    dbConnect()
    updateQuery = "UPDATE details SET name=%s,age=%s,gender=%s,contact=%s WHERE ID=%s;"
    tb_cursor.execute(updateQuery,(name,age,gender,contact,id))
    db_connection.commit()
    dbDisconnect()
    return True

def deleteDetailFromTable(id):
    dbConnect()
    deleteQuery = "DELETE FROM details WHERE ID=%s;"
    tb_cursor.execute(deleteQuery,(id))
    db_connection.commit()
    dbDisconnect()
    return True



if __name__=="__main__":
    app.run(debug=True)