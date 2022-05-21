from flask import render_template, redirect, session, request, flash

from flask_app import app

from flask_app.models import user, car

@app.route('/new')
def add_new_car():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('new_car.html', user=user.User.get_by_user_id(data))

@app.route('/new/create', methods=['POST'])
def create_new_sale():
    if 'user_id' not in session:
        return redirect('/logout')
    if not car.Car.validate_car(request.form):
        return redirect('/new')
    data = {
        'price' : int(request.form['price']),
        'model' : request.form['model'],
        'make' : request.form['make'],
        'year' : int(request.form['year']),
        'description' : request.form['description'],
        'user_id' : session['user_id']
    }
    car.Car.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('edit_post.html', user=user.User.get_by_user_id(user_data), car=car.Car.get_by_car_id(data))

@app.route('/update/post', methods=['POST'])
def update_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not car.Car.validate_car(request.form):
        return redirect(f'/edit/{request.form["id"]}')
    data = {
        'price' : int(request.form['price']),
        'model' : request.form['model'],
        'make' : request.form['make'],
        'year' : int(request.form['year']),
        'description' : request.form['description'],
        'id' : request.form['id']
    }
    car.Car.update(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data= {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('view_post.html', user=user.User.get_by_user_id(user_data),cars=car.Car.get_all_cars(), car=car.Car.get_by_car_id(data))

@app.route('/delete/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    car.Car.delete(data)
    return redirect('/dashboard')