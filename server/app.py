# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.filter(Earthquake.id==id).first()
    if earthquake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    
    # convert to json
    earthquake_data = {
        "id": earthquake.id,
        "location": earthquake.location,
        "magnitude": earthquake.magnitude,
        "year": earthquake.year
    }
    earthquake_json = jsonify(earthquake_data)
    return earthquake_json, 200

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    # response_body = [quake.to_dict() for quake in earthquakes]
    response_body = {
        "count": len(earthquakes),
        "quakes": [quake.to_dict() for quake in earthquakes]
    }
    return make_response(response_body, 200)

#     earthquakes_data = {
#         "count": len(earthquakes)
#         "quakes":[
#             {
#                 "id": earthquake.id,
#                 "location": earthquake.location,
#                 "magnitude": earthquake.magnitude,
#                 "year": earthquake.year
#             }
#         ]
#     }

# @app.route("/hotels")
# def get_hotels():
#     hotels = Hotel.query.all()
#     response_body = [hotel.to_dict(rules='-id',) for hotel in hotels]
#     return make_response(response_body)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
