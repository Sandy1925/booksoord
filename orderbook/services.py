import datetime
from filestack.utils import requests

from .models import Cart,Order


"""
Converting dictionary to Entity of cart and order
parm: cart/order dictionary ,cart or order object
Author:Santhosh  Kumar
Date Created: 14/01/24
Date Modified:
"""

def dictToEnt(data,object):
    for attr,value in data.items():
        setattr(object,attr,value)
    return object

"""
Converting Cart into Order
param: cart
author:Santhosh Kumar
Date Created: 15/01/24
Date Modified:
"""
def cartToOrder(data):
    order = Order()
    order.bookCode = data.bookCode
    order.customerCode = data.customerCode
    order.quantity = data.quantity
    book = requests.get("http://localhost:8000/api/getByCode/" + data.bookCode).json()
    order.price = book['price']
    order.total = (order.quantity * order.price) + book['rating'] * 10
    order.status = 1
    order.dateOrd = datetime.date.today()
    order.save()
    return order

"""
Checking cart existence
param: Cart
Author:Santhosh Kumar
Date Created: 18/04/2024
Date Modified:
"""
def checkCartAlreadyExists(data):

    carts=Cart.objects.filter(customerCode=data.customerCode).values()
    resultCart=list(map(lambda b:dictToEnt(b,Cart()),carts))
    result=getCustomerCart(data,resultCart)
    return result

"""
Getting particular Customer
Author:Santhosh Kumar
Date Created: 18/04/2024
Date Modified:
"""
def getCustomerCart(data,cartList):
    for i in cartList:
        if i.customerCode==data.customerCode and i.bookCode==data.bookCode:
            return i


