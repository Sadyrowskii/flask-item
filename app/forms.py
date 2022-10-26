from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, SelectField, DateField, ValidationError, validators

from .models import Item


class ItemForm(FlaskForm):
    name = StringField(label='Название товара',validators=[validators.data_required()])
    price = IntegerField(label='Цена товара', validators=[validators.data_required()])
    submit = SubmitField(label='Сохранить товар', validators=[validators.data_required()])


class PurchaseForm(FlaskForm):
    name = StringField(label='Имя клиента')
    age = IntegerField(label='возраст')
    item_id = SelectField(label='Что купил')
    date_purchase = DateField('Дата')
    submit = SubmitField(label='Сохранить покупку')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        result = []
        for item in Item.query.all():
            result.append((item.id, item.name))
        self.item_id.choices = result


    # def validate_price(self, price):
    #    if price.data < 100:
    #     raise ValidationError(' Товар не может  стоить меньше 100 единиц ')















    def age_years(self, age):
        if age.data < 18:
            raise ValidationError('Доступ только пользователям которым старше 18 лет')
