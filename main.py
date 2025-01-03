from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video are required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video are required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        video = VideoModel.query.get(video_id)
        if not video:
            abort(404, message="Could not find video with that ID.")
        return video

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        video = VideoModel.query.get(video_id)
        if video:
            video.name = args['name']
            video.views = args['views']
            video.likes = args['likes']
        else:
            video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
            db.session.add(video)
        db.session.commit()
        return video, 201


    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        video = VideoModel.query.get(video_id)
        if not video:
            abort(404, message="Could not find video with that ID, cannot edit.")
        if args['name']:
            video.name = args['name']
        if args['views']:
            video.views = args['views']
        if args['likes']:
            video.likes = args['likes']
        db.session.commit()
        return video

    def delete(self, video_id):
        video = VideoModel.query.get(video_id)
        if not video:
            abort(404, message="Could not find video with that ID.")
        db.session.delete(video)
        db.session.commit()
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
