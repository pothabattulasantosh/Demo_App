from flask import Flask, jsonify, request,make_response,render_template #Flask
from flask_restful import Api, Resource #flask_restful
import flask
import utils
from pymongo import MongoClient

clinet=MongoClient("mongodb://db:27017")
db  = clinet.usersDB
users = db["Users"]




app = Flask(__name__)
api = Api(app)


class Check_toxicity(Resource):
    def get(self):
        return make_response(render_template('main_page.html'))

    def post(self):
        get_data = request.form.to_dict()
        name = get_data['name']
        comment = get_data['comment']
        validated = utils.validateParams(name=name,comment=comment)
        if validated['status']!=200:
            return jsonify(validated)
        proccessed_cmt = utils.preProcess(comment=comment)
        eval_cmt = utils.evaluteToxicity(proccessed_cmt)
        result = {"name":name,"cmt":eval_cmt}
        users.insert({
        "Name":name,
        "Comment":comment,
        "cleaned_text":proccessed_cmt,
        "judgement": eval_cmt

        })

        return make_response(render_template('display_result.html',result=result))

api.add_resource(Check_toxicity, '/','/check_toxicity')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
