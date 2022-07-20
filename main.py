from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#  Cafe TABLE Configuration
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
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def welcome():
    return jsonify(welcome={"flask": "APi cafes"})


@app.route("/random")
def home():
    all_data = db.session.query(Cafe).all()
    random_cafe = random.choice(all_data)
    return jsonify(cafe=random_cafe.to_dict())
    

## HTTP GET - Read Record
@app.route("/all")
def all_cafe():
    all_data = db.session.query(Cafe).all()
    cafes_data = [i.to_dict() for i in all_data]
    return jsonify(cafes=cafes_data)


@app.route("/search")
def search():
    query_location = request.args.get("loc")
    cafe_data = db.session.query(Cafe).filter_by(location=query_location).all()
    location_cafe = [i.to_dict() for i in cafe_data]

    if location_cafe:
        return jsonify(cafe=location_cafe)
    else:
        return jsonify(error={"Not found": "This is no hotel in this location."})


## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        id=request.form.get(""),
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record
@app.route("/update/<int:cafe_id>", methods=["PATCH"])
def edit(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.query(Cafe).filter_by(id=cafe_id).first()
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify({"success": "Successfully update the price."})
    else:
        return jsonify(error={"Not found": "this data is not present in database."})



## HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    api_key = request.args.get("api_key")
    if api_key == "TopSecretAPIKey":
        cafe = db.session.query(Cafe).filter_by(id=cafe_id).first()
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify({"success": "Successfully deleted"}), 200
        else:
            return jsonify({"Not found": f"This id={cafe_id} not present in database."}), 404
    else:
        return jsonify({"Apikey wrong": "You don't have permission to delete."}), 403


if __name__ == '__main__':
    app.run(debug=True)
