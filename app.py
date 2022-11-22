from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
 
db = SQLAlchemy(app)


class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
 
    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr
        

@app.route('/')
def hello():
    return render_template("index.html")
 
@app.route('/about')
def about():
    return render_template("about.html",ar=Students.query.all()) #i put the ar here because i want to display it in the "about" page
 
@app.route('/add',methods=["POST","GET"])
def add():
    if request.method == "POST":
        name = request.form.get('name')
        city = request.form.get('city')
        addr = request.form.get('addr')
    
        newStudent= Students(name,city,addr)
        db.session.add (newStudent)
        db.session.commit()
        return render_template("about.html",ar=Students.query.all())
    else:
        return render_template("add.html")

@app.route("/del/<ind>", methods=['DELETE','GET'])
def del_student(ind=-1):
        del_student=Students.query.get(int(ind))
        msg=f"no such student"
        if del_student:
            db.session.delete(del_student)
            db.session.commit()
            msg=f"student del {del_student.name}"
            return render_template("about.html",ar=Students.query.all(),msg=msg) 
        return render_template("about.html",ar=Students.query.all(),msg=msg)  
        



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True,port=8000)
    

