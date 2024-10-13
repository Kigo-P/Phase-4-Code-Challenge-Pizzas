#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# instantiating the api with the app
api = Api(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# creating a Restaurants resource
class Restaurants(Resource):
    #  using get method to get all the restaurants
    def get(self):
        # querying the Restaurant model to get all the restaurants
        restaurants = Restaurant.query.all()
        # Looping through the restaurants to get each restaurant. Converting each restaurant to a dict and setting serialize rules for better display
        restaurant = [restaurant.to_dict(rules=("-restaurant_pizzas", )) for restaurant in restaurants]
        #  creating and returning a response
        response = make_response(restaurant, 200)
        return response
    pass

#  creating a RestaurantById resource
class RestaurantsById(Resource):
    # using get method to get a restaurant by the id 
    def get(self, id):
        # querying and filtering the restaurant by the id
        restaurant = Restaurant.query.filter_by(id = id).first()
        if restaurant:
            #  making the restaurant to a dictionary using to_dict()
            restaurant_dict= restaurant.to_dict()
            # creating and returning a response
            response = make_response(restaurant_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "Restaurant not found"}
            response = make_response(response_body, 404)
            return response
        
    # using a delete method to delete an existing restaurant
    def delete(self, id):
        # querying and filtering the restaurant by the id
        restaurant = Restaurant.query.filter_by(id = id).first()
        if restaurant:
            #  deleting the restaurant and commiting the changes to the database
            db.session.delete(restaurant)
            db.session.commit()
            #  creating and returning a response based on the response body
            response_body = {"message":"Restaurant deleted successfully"}
            response = make_response(response_body, 204)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "Restaurant not found"}
            response = make_response(response_body, 404)
            return response
    pass

# creating a Pizzas resource
class Pizzas(Resource):
    # using get method to get all the pizzas
    def get(self):
        # querying the Pizza model to get all the pizzas
        pizzas = Pizza.query.all()
        # Looping through the pizzas to get each pizza. Converting each pizza to a dict and setting serialize rules for better display
        pizza = [pizza.to_dict(rules=("-restaurant_pizzas", )) for pizza in pizzas ]
        # creating and returning a response 
        response = make_response(pizza, 200)
        return response
    pass

# creating a RestaurantPizzas resource
class RestaurantPizzas(Resource):
    # creating a post method that posts the new restaurant pizza
    def post(self):
        # getting the price of pizza based on the request
        data = request.get_json()
        price = data["price"]
        # creating a conditional that checks is the price is valid. If it is valid create a new restaurant pizza elae return an error message
        if price >=1 and price <=30:
            new_restaurant_pizza = RestaurantPizza(
            price = price,
            pizza_id = data["pizza_id"],
            restaurant_id= data["restaurant_id"]
            )
            if new_restaurant_pizza:
                #  adding and commiting the new restaurant to the database
                db.session.add(new_restaurant_pizza)
                db.session.commit()

                # making the new_restaurant pizza to a dictionary using to_dict() method
                new_restaurant_pizza_dict = new_restaurant_pizza.to_dict()

                # creating and returning a response 
                response = make_response(new_restaurant_pizza_dict, 201)
                return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"errors": ["validation errors"]}
            response = make_response(response_body, 400)
            return response


    pass


# adding resource and routes to the specific Resources 
api.add_resource(Restaurants, "/restaurants", endpoint="restaurants")
api.add_resource(RestaurantsById, "/restaurants/<int:id>", endpoint="restaurants_by_id")
api.add_resource(Pizzas, "/pizzas", endpoint="pizzas")
api.add_resource(RestaurantPizzas, "/restaurant_pizzas", endpoint="restaurant_pizzas")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
