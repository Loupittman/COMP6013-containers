from html import escape


from flask import Flask, abort, make_response
from flask.json import dumps, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

__version__ = '0.0.0.g4058e57'

app = Flask(__name__)
api= Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://18059081:dn46d93bnmxx@localhost/container_identification'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
db = SQLAlchemy(app)


class Container(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    container_id = db.Column(db.String(12), unique=True, nullable=False)
    type = db.Column(db.String(30))
    description = db.Column(db.String(256))
    vle = db.Column(db.String(16))
    model_mix = db.Column(db.String(45))
    empties_storage = db.Column(db.String(45))
    empties_lane = db.Column(db.String(30))
    jis_route = db.Column(db.String(8))
    length = db.Column(db.Numeric(10, 1))
    width = db.Column(db.Numeric(10, 1))
    height = db.Column(db.Numeric(10, 1))
    weight = db.Column(db.Numeric(10, 1))
    haulier_id = db.Column(db.Integer())
    load_unit_id = db.Column(db.Integer())

    def as_dict(self):
        # Does not follow relationships or encode primary or foreign keys but that's all we need for now
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


containers_put_args = reqparse.RequestParser()
containers_put_args.add_argument("id", type=int, help="container ID")
containers_put_args.add_argument("type", type=str, help="type of container")
containers_put_args.add_argument("description", type=str, help="container description")

containers = {}


class ContainerTest(Resource):
    def get(self, container_id):
        return containers[int(container_id)]

    def put(self, container_id):
        args = containers_put_args.parse_args()
        return{container_id: args}


api.add_resource(ContainerTest, "/containertest/<container_id>")


@app.route('/container/<container_id>', methods=['GET'])
def container(container_id):
    c = Container.query.filter_by(container_id=container_id).first()
    if not c:
        abort(make_response(jsonify({"code" : "404", "message" : f'Container ID {container_id} not found'}), 404))

    response = make_response(jsonify(c.as_dict()).data.decode('UTF-8'))
    response.mimetype = 'application/json'
    return response


