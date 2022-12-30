from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
API_KEY = "TestingAPIKey"

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

    # Helper function that changes all attributes in a cafe object into a dict
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
# Updates a cafe with cafe_id with new coffee_price
@app.route('/update-price/<cafe_id>', methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get('new_price')
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated coffee price."}), 200
    else:
        return jsonify(error={"Not found": "Sorry, that cafe id was not found."}), 404

## HTTP DELETE - Delete Record

@app.route('/report-closed/<cafe_id>', methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe = db.session.query(Cafe).get(cafe_id)
    api_key = request.args.get('api-key')
    if api_key == API_KEY:
        if cafe:
            # Delete entry in DB
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Cafe successfully deleted."}), 200
        else:
            return jsonify(error={"Not Found": "Unable to find cafe with that id."}), 404
    else:
        return jsonify(error={"error": "Sorry, you do not have a valid API Key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
