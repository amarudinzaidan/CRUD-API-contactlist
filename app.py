# Import required modules
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint


# Create a flask object
app = Flask(__name__)


# Set app.config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Create flask swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "ContactList API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


# Create a db instace
db = SQLAlchemy(app)


# Create a ma instance
ma = Marshmallow(app)


# Create a model
class ContactList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200))
    lastName = db.Column(db.String(200))
    numberPhone = db.Column(db.String(200))
    address = db.Column(db.String(300))


# Create db schema class
class ContactListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'numberPhone', 'address')


# Create schema objects for contactlist and contactlists
contactlist_schema = ContactListSchema(many=False)
contactlists_schema = ContactListSchema(many=True)


# Dealing with errors
@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)

@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)

@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


# Add a contact
@app.route("/contactlist", methods=["POST"])
def add_contact():
    try:
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        numberPhone = request.json['numberPhone']
        address = request.json['address']

        new_contact = ContactList(firstName=firstName, lastName=lastName, numberPhone=numberPhone, address=address)

        db.session.add(new_contact)
        db.session.commit()
        return contactlist_schema.jsonify(new_contact)

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})


# Get all contacts
@app.route("/contactlist", methods=["GET"])
def get_contacts():
    contacts = ContactList.query.all()
    result_set = contactlists_schema.dump(contacts)
    return jsonify(result_set)

# Get a specific contact
@app.route("/contactlist/<int:id>", methods=["GET"])
def get_contact(id):
    contact = ContactList.query.get_or_404(int(id))
    return contactlist_schema.jsonify(contact)


# Update a contact
@app.route("/contactlist/<int:id>", methods=["PUT"])
def update_contact(id):
    contact = ContactList.query.get_or_404(int(id))

    try:
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        numberPhone = request.json['numberPhone']
        address = request.json['address']

        contact.firstName = firstName
        contact.lastName  = lastName
        contact.numberPhone = numberPhone
        contact.address = address

        db.session.commit()
    except Exception as e:
        return jsonify({"Error": "Invalid request, please try again."})

    return contactlist_schema.jsonify(contact)


# Delete contact
@app.route("/contactlist/<int:id>", methods=["DELETE"])
def delete_contact(id):
    contact = ContactList.query.get_or_404(int(id))
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"Success": "contact deleted."})

if __name__ == "__main__":
    app.run(debug = True)