from flask import Flask,render_template,flash,redirect,url_for,request
from wtforms import Form,StringField,TextAreaField,validators
from flask_googlemaps import Map
from flask_googlemaps import GoogleMaps
import os

class ContactForm(Form):
    name = StringField("Adınız",validators=[validators.Length(min=4,max=25)])
    surname = StringField("Soyadınız",validators=[validators.Length(min=5,max=35)])
    email = StringField("Email Adresiniz",validators=[validators.Email(message="Lütfen geçerli bir email adresi giriniz.")]) 
    message = TextAreaField("Mesajınız",validators=[validators.length(min=10)])

app = Flask(__name__)
app.secret_key = "EKS"

app.config['GOOGLEMAPS_KEY'] = "AIzaSyDWcEoJfhD7DchMWeerGixj28NUa4U1tYA"

GoogleMaps(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact", methods = ["GET","POST"])
def contact():
    mymap= Map(
         identifier="view-side",  # for DOM element
        varname="mymap",  # for JS object name
        style=(
            "height:500px;"
            "width:500px;"
        ),
        lat=37.771663,
        lng=30.556486,
        markers=[(37.771663, 30.556486)],
    )
    form = ContactForm(request.form)
    if request.method == "POST":
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        message = form.message.data

        mail=name +";"+ surname +";"+ email +";"+ message +";\n"

        with open('messages.txt', 'a', encoding="utf-8") as f:
            f.write(str(mail))
        
        flash("Mesajınız Başarılıyla İletildi. Teşekkür Ederiz...","success")

        return redirect(url_for("messagebox"))
    else:
        return render_template("contact.html", form = form, mymap = mymap)

@app.route("/messagebox", methods = ["GET","POST"])
def messagebox():
    mails = []
    with open('messages.txt', 'r', encoding="utf-8") as f:
            for i in f:
                satir = i[:-1]
                mails.append(satir.split(";"))

    return render_template("/messagebox.html", mails = mails)

@app.route("/album")
def album():
    return render_template("album.html")

@app.route("/education")
def education():
    return render_template("education.html")

@app.route("/notes")
def notes():
    return render_template("notes.html")

@app.route("/hobby")
def hobby():
    return render_template("hobby.html")

if __name__=="__main__":
    app.run(debug=True)