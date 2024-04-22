from ninja import Schema,ModelSchema
from .models import Cart,Order

class CartIn(ModelSchema):
    class Meta:
        model=Cart
        fields='__all__'


class CartOut(ModelSchema):
    class Meta:
        model=Cart
        fields='__all__'





class OrderIn(ModelSchema):
    class Meta:
        model=Order
        fields=['bookCode','customerCode','quantity']

class OrderOut(ModelSchema):
    class Meta:
        model=Order
        fields='__all__'