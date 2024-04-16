import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
'''
@FIXME: This typically means that you attempted to use functionality that needed                                                
the current application. To solve this, set up an application context                                                   
with app.app_context(). See the documentation for more information.    
'''
app.app_context().push() 

'''
@uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

def get_drinks_short():
    drinks = Drink.query.all()
    drink_list = []
    for drink in drinks:
        drink_list.append(drink.short())
    return drink_list

def get_drinks_long():
    drinks = Drink.query.all()
    drink_list = []
    for drink in drinks:
        drink_list.append(drink.long())
    return drink_list
# ROUTES
'''
@Implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    print("hello")
    return jsonify({
        'success': True,
        'drinks': get_drinks_short()
    }), 200

'''
Implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drink-details')
def get_drinks_detail(token):
    return jsonify({
        'success': True,
        'drinks': get_drinks_long()
    }), 200
'''
Implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(token):
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)
    # Make new drink
    new_drink = Drink(title = title, recipe=json.dumps([recipe]))
    # Add to database
    new_drink.insert()
    return jsonify({
        'success': True,
        'drinks': new_drink.long()
    }), 200
'''
Implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drink_id>", methods =['PATCH'])
@requires_auth('patch:drinks')
# decorator return f(payload, *args, **kwargs), so make dump_param to avoid error 
def patch_update_drink(dump_param, drink_id):
    # find for available id
    try:
        drink = Drink.query.get(drink_id)
        if not drink:
            abort(404)
        # Get informative mofidication
        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        # Modify 
        if title:
            drink.title = title
        if recipe:
            drink.recipe = json.dumps([recipe])
        print(drink.title)
        print(drink.recipe)
        # Update the drink
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except:
        abort(500)

@app.route('/drinks/<int:drink_id>', methods =['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(dump_param, drink_id):
    # find for available id
    try:
        drink = Drink.query.get(drink_id)
        if not drink:
            abort(404)
        # Delete the drink
        drink.delete()
        return jsonify({
            'success': True,
            'drinks': drink_id
        }), 200
    except:
        abort(500)

# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 422

@app.errorhandler(AuthError)
def authorize_error(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Permission denied"
    }), 403

@app.errorhandler(500)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500
