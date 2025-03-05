from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from market import app, db
from market.models import User, Item
from market.forms import RegisterForm, LoginForm, PurchaseItem, SellItem

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")

@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItem()
    selling_form = SellItem()

    if request.method == 'POST':
        # Purchasing Logic
        purchased_item = request.form.get('purchased_item')
        if purchased_item:
            purchased_item_object = Item.query.filter_by(name=purchased_item).first()
            if purchased_item_object:
                if current_user.can_purchase(purchased_item_object):
                    purchased_item_object.buy(current_user)
                    flash(f'Congrats! you purchased {purchased_item_object.name} for {purchased_item_object.price}$.', category="success")
                else:
                    flash(f"Unfortunately, you don't have enough money to purchase {purchased_item_object.name}", category='danger')

        # Selling Logic
        sold_item = request.form.get('sold_item')
        if sold_item:
            sold_item_object = Item.query.filter_by(name=sold_item).first()
            if sold_item_object:
                if current_user.can_sell(sold_item_object):
                    sold_item_object.sell(current_user)
                    flash(f'Congrats! you sold {sold_item_object.name} for {sold_item_object.price}$.', category="success")
                else:
                    flash(f"Unfortunately, something went wrong while trying to sell your item! Please try again.", category='danger')

        return redirect(url_for('market_page'))

    # GET request logic
    items = Item.query.filter_by(owner=None)
    owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route("/register", methods=['GET', 'POST'])
def register_form():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for("market_page"))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg[0]}', category='danger')
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again.', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out.", category='info')
    return redirect(url_for("home_page"))