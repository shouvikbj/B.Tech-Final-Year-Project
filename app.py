from flask import Flask,render_template,redirect,request,url_for,session
import csv
import delete as dlt
import loginDB
import smtplib
import os

app = Flask(__name__, static_url_path='')
app.secret_key = 'this is a secret key'

#APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template("login.html")

@app.route("/home")
def home():
    if 'username' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('login'))

@app.route("/login", methods = ["POST","GET"])
def login():
    return render_template("login.html")

@app.route("/getin", methods = ["POST","GET"])
def getin():
    username = request.form.get("username")
    password = request.form.get("password")
    details = loginDB.login(username)
    if(username==details[0][0] and password==details[0][1]):
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return render_template("failure.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/register", methods = ["POST","GET"])
def register():
    firstname = request.form.get("fname")
    lastname = request.form.get("lname")
    email = request.form.get("email")
    phone = request.form.get("pnumber")
    password = request.form.get("password")
    username = email[:email.find("@")]
    image = "defaultProfileImage.png"
    
    file = open("users.csv","a")
    writer = csv.writer(file)
    file2 = open("users.csv","r")
    reader = csv.reader(file2)
    test = False
    for line in reader:
        if(username == line[0]):
            test = True

    if(test):
        file.close()
        file2.close()
        return  render_template("tryagain.html")
    
    else:
        writer.writerow((username,firstname,lastname,email,phone,password,image))
        loginDB.createUser(username,firstname,lastname,email,phone,password,image)

        file.close()

        message = "To Login into \"GangPayee\" WebApp \n\nUSERNAME : {}.\n\nRegards from, \nTeam \"GangPayee\""
        message1 = message.format(username)
        message2 = "A new User just registered. \nCheckout."

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login('services.shouvikbajpayee@gmail.com', 'maathakur60@')
        server.sendmail('services.shouvikbajpayee@gmail.com', email, message1)
        server.sendmail('services.shouvikbajpayee@gmail.com', 'bajpayeeshouvik@gmail.com', message2)
        server.close()

        return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")

@app.route("/sendpass", methods = ["POST","GET"])
def sendpassword():
    return redirect(url_for('login'))

@app.route("/account")
def account():
    if 'username' in session:
        user = loginDB.getUser(session['username'])
        #image = "defaultProfileImage.png"
        firstname = user[0][1]
        lastname = user[0][2]
        email = user[0][3]
        phone = user[0][4]
        image = user[0][6]

        return render_template("account.html",firstname=firstname,lastname=lastname,email=email,phone=phone,image=image)
    else:
        return redirect(url_for('login'))

@app.route("/uploadProfilePic", methods=["POST"])
def uploadProfilePic():
    if 'username' in session:
        target = 'static/imges/profilePics'
        #if not os.path.isdir(target):
            #os.mkdir(target)

        file = request.files.get("file")
        if(file):
            filename = file.filename
            destination = "/".join([target,filename])
            file.save(destination)

            loginDB.updateProfilePic(session['username'], filename)
            
            dlt.deleteRedundantImages()

            return redirect(url_for('account'))
        else:
            return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))

@app.route("/updateDetails", methods = ["POST","GET"])
def updateDetails():
    return redirect(url_for('account'))

@app.route("/customsearch")
def customsearch():
    if 'username' in session:
        return render_template("customsearch.html")
    else:
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)