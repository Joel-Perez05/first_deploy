from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user

from flask import flash

class Car:
    db = "car_dealz"
    def __init__(self, data):
        self.id = data['id'] 
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        
    @classmethod
    def get_all_cars(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        cars = []
        for row in results:
            car = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            car.user = user.User(user_data)
            cars.append(car)
        return cars
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO cars (price, model, make, year, description, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE cars SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    
    @classmethod
    def get_by_car_id(cls,data):
        query = "SELECT * FROM cars WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_car(car):
        is_valid = True
        if str(car['price']) == '' or int(car['price']) <= 0:
            flash('car price must be greater than 0', 'create')
            is_valid = False
        if len(car['model']) < 2:
            flash('car model must include at least 2 characters', 'create')
            is_valid = False
        if len(car['make']) < 2:
            flash('car make must include at least 2 characters', 'create')
            is_valid = False
        if str(car['year']) == '' or int(car['year']) <= 1900:
            flash("car year must be greater than 1900's", "create")
            is_valid = False
        if len(car['description']) < 3:
            flash('car description must have at least 3 characters', 'create')
            is_valid = False
        return is_valid