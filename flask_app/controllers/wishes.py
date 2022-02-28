from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.wish import Wish

@app.route('/wish/new')
def new_wish():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    context = {
        'user':User.get_users_by_id(data)
    }
    return render_template('create_wish.html', **context)

@app.route('/wish/create',methods=['POST'])
def create_wish():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Wish.validate_wish(request.form):
        return redirect('/wish/new')
    data = {
        "wish": request.form["wish"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    Wish.save_wish(data)
    return redirect('/dashboard')

@app.route('/wish/edit/<int:id>')
def edit_wish(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    data = {
        "id":id
    }
    context = {
        "edit" : Wish.get_one_wish(data),
        "user" : User.get_users_by_id(user_data)
    }
    return render_template("edit_wish.html", **context)

@app.route('/wish/update',methods=['POST'])
def update_wish():
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = request.form['id']
    if not Wish.validate_wish(request.form):
        return redirect(f'/wish/edit/{user_id}')
    data = {
        "id": request.form['id'],
        "wish": request.form["wish"],
        "description": request.form["description"]
    }
    Wish.update_wish(data)
    return redirect('/dashboard')

@app.route('/wish/<int:user_id>')
def all_wishes_posted_by_one_author(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id":user_id,
    }
    user_data = {
        "id":session['user_id']
    }
    context = {
        "wishes" : Wish.get_all_wishes_by_one_poster(data),
        "user" : User.get_by_id(user_data),
    }
    return render_template("user_wish.html", **context)

@app.route('/wish/destroy/<int:id>')
def destroy_wish(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Wish.destroy_wish(data)
    return redirect('/dashboard')

# @app.route('/like_wish/<int:wish_id>')
# def increase_like(wish_id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         'wish_id' : wish_id,
#         'user_id' : session['user_id'],
#     }
#     Wish.like_wish(data)
#     return redirect('/dashboard')


# @app.route('/grant_wish', methods=['POST'])
# def grant_wish():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     user_id = request.form['id']
#     if not Wish.validate_wish(request.form):
#         return redirect(f'/wish/edit/{user_id}')
#     data = {
#         "id": request.form['id'],
#         "wish": request.form["wish"],
#         "description": request.form["description"]
#     }
#     Wish.grant_wish(data)
#     return redirect('/dashboard')
