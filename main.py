from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Café TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # dictionary = {}
        # for column in self.__table__.columns:
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary
        return {column.name: getattr(self,column.name) for column in self.__table__.columns}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods=["GET"])
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)

    # Use jsonify() to turn SQLAlchemy object into a JSON via serialization:
    # new_json = jsonify(cafe={
    #     'can_take_calls': random_cafe.can_take_calls,
    #     'coffee_price': random_cafe.coffee_price,
    #     'has_sockets': random_cafe.has_sockets,
    #     'has_toilet': random_cafe.has_toilet,
    #     'has_wifi': random_cafe.has_wifi,
    #     # 'id': random_cafe.id,
    #     'img_url': random_cafe.img_url,
    #     'location': random_cafe.location,
    #     'map_url': random_cafe.map_url,
    #     'name': random_cafe.name,
    #     'seats': random_cafe.seats
    #     }
    # )
    return jsonify(cafe=random_cafe.to_dict())

## HTTP GET - Read Record
# Returns all cafes in database
@app.route("/all", methods=["GET"])
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    all_cafes_dict = []
    for cafe in cafes:
        all_cafes_dict.append(cafe.to_dict())
    return jsonify(cafes=all_cafes_dict)

# Searches for a cafe
@app.route('/search/', methods=["GET"])
def search_cafes():
    loc = request.args.get('loc').title()
    result = db.session.query(Cafe).filter_by(location=loc).first()
    if result:
        return jsonify(cafe=result.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, there is not a cafe at that location."})


## HTTP POST - Create Record
# Create a new cafe in the database
@app.route('/add', methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
        name= request.form.get("name"),
        map_url= request.form.get("map_url"),
        img_url= request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        coffee_price=request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added new cafe."})

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
