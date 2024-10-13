from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    # a relationship that maps restaurant to related restaurant_pizzas- Do cascade since it is the parent
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="restaurant", cascade="all, delete-orphan")

    # add serialization rules
    serialize_rules = ("-restaurant_pizzas.restaurant", )

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    # a relationship that maps pizza to related restaurant_pizzas- Do cascade since it is the parent
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="pizza", cascade="all, delete-orphan")

    # add serialization rules
    serialize_rules = ("-restaurant_pizzas.pizza", )

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    #  Foreign key that stores the pizza id
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    # Foreign key that stores the restaurant id
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))

    # add relationships
    # a relationship that maps resturantpizzas to a related pizza
    pizza = db.relationship("Pizza", back_populates = "restaurant_pizzas")
    # a relationship that maps restaurantpizzas to a related restaurant
    restaurant = db.relationship("Restaurant", back_populates = "restaurant_pizzas")

    # add serialization rules
    serialize_rules = ("-pizza.restaurant_pizzas", "-restaurant.restaurant_pizzas", )

    # add validation
    #  creating a validation for the price to be between 1 and 30
    @validates("price")
    def validates_price(self, key, price):
        if price < 1 or price >30:
            raise ValueError ("Price must be between 1 and  30")
        return price


    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'
