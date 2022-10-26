import datetime

from flask import render_template, request, redirect, url_for, flash
from . import app, db
from .models import Purchase, Item
from .forms import PurchaseForm, ItemForm





def purchase_views():
    title = 'Список Клиентов'
    purchases = Purchase.query.all()
    return render_template('purchase.html', purchases=purchases, title=title)

def get_single_purchase(purchase_id):
    purchase = Purchase.query.filter_by(id=purchase_id).first()
    return render_template('single_purchase.html', purchase=purchase)

def purchase_create():
    title = 'Изменть данные клиента'
    form = PurchaseForm(request.data)
    if request.method == 'POST':
        form.validate_on_submit()
        purchase = Purchase()
        form.populate_obj(purchase)
        db.session.add(purchase)
        db.session.commit()
        return redirect(url_for('purchase'))


def update_single_purchase(purchase_id):
    purchase = Purchase.query.filter_by(id=purchase_id).first()
    form = PurchaseForm()
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        purchase.name = name
        purchase.age = age
        db.session.commit()
        return redirect(url_for('single_purchase', purchase_id=purchase.id))
    else:
        for field, errors in form.errors.purchase():
            for error in errors:
                flash(f'Ошибка в поле {field} текст ошибки {error}', 'danjer')
                return render_template('update_single_purchase.html')

def delete_single_purchase(purchase_id):
    purchase = Purchase.query.filter_by(id=purchase_id).first()
    form = PurchaseForm()
    if request.method == 'GET':
        return render_template('delete_purchase.html', purchase=purchase, form=form)
    if request.method == 'POST':
        db.session.delete(purchase)
        db.session.commit()
        flash(f'Данные о продажах под номером {purchase.id} успешно удалены', 'success')
        return redirect(url_for('purchase'))

def item_views():
    title = 'Список товаров'
    items = Item.query.all()
    return render_template('items.html', items=items, title=title)


def item_create():
    title = 'Добавление товара'
    form = ItemForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_item= Item()
            form.populate_obj(new_item)
            db.session.add(new_item)
            db.session.commit()
            flash(f'Товар под номером {new_item.id}успешно добавлен', 'success')
            return redirect(url_for('item'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Ошибка в  поле {field} текст ошибки{error}', 'danger')
    return render_template('item_form.html', form=form, title=title)

def get_single_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    return render_template('single_item.html', item=item)


def update_single_item(item_id):

    item = Item.query.filter_by(id=item_id).first()
    form = ItemForm(request.form, obj=item)
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        item.name = name
        item.price = price
        db.session.commit()
        flash(f'Товар под номером {item_id}успешно обнавлен')
        return redirect(url_for('single_item', item_id=item.id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в  поле {field} текст ошибки{error}', 'danger')
    return render_template('item_form.html', form=form, item=item)



def delete_single_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if request.method == 'GET':
        return render_template('delete_item.html', item=item)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('item'))

