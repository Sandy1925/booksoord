import datetime
from datetime import date

from django.shortcuts import render
# Create your views here.
from filestack.utils import requests
from ninja import NinjaAPI
from .schemas import CartIn, CartOut, OrderIn, OrderOut
from .services import dictToEnt, cartToOrder, checkCartAlreadyExists
from .models import Cart,Order
from typing import List
api=NinjaAPI()


"""
Adding items to cart
Param :CartIn
Author: Santosh Kumar
Date Created: 15/01/24
Date Modified:
"""

""" finalResult=OutputCart()
  finalResult.bookCode=result.bookCode
  finalResult.customerCode=result.customerCode
  finalResult.quantity=result.quantity
  finalResult.title=book['title']
  finalResult.author=book['author']
  finalResult.price=book['price']"""
@api.post("newCart",response=CartOut)
def newCart(request,data:CartIn):
    result=checkCartAlreadyExists(data)
    if ( result is not None):
        result.quantity+=data.quantity
        result.save()
    else:
        result=dictToEnt(data.__dict__,Cart())
        result.save()

    return result

"""
Getting Cart by CustomerCode
Param:CustomerCode
Author:Santhosh Kumar
Date Created: 15/01/24
Date Modified:
"""
@api.get("getByCusCode/{cusCode}",response=List[CartOut])
def getCartByCusCode(request,cusCode:str):
    data=Cart.objects.filter(customerCode=cusCode).values()
    result=list(map(lambda b: dictToEnt(b,Cart()),data))
    #resultSet=list(map(lambda b:cartToOutputCart(b),result))
    return  result

"""
Clearing Cart by Customer Code
Param:customer Code
Author:Santhosh Kumar
Date Created: 15/01/24
Date Modified:
"""
@api.delete("delByCusCode/{cusCode}")
def clearCartByCusCode(request,cusCode:str):
    data=Cart.objects.filter(customerCode=cusCode).values()
    result=list(map(lambda b:dictToEnt(b.__dict__,Cart()),data))
    for i in result:
        i.delete()
    return {"message":"Cart Cleared Successfully"}

@api.delete("delByCusAndCart/{cusCode}/{bookCode}")
def deleteIndividual(request,cusCode:str,bookCode:str):
    data=Cart.objects.filter(customerCode=cusCode).values()
    result=list(map(lambda b:dictToEnt(b,Cart()),data))
    for i in result:
        if i.bookCode == bookCode:
            i.delete()
            break
    return {"message":"Cart cleared successfully"}

"""
Placing new Order with  cart and customer  code
param: customer Code
Author: Santhosh Kumar
Date Created: 15/01/24
Date Modified:
"""
@api.post("newOrder/{cusCode}",response=List[OrderOut])
def newOrder(request,cusCode:str):
    data=getCartByCusCode(request,cusCode)
    result=list(map(lambda c:cartToOrder(c),data ))
    clearCartByCusCode(request,cusCode)
    return result

"""
Creating order with order
Param: OrderIn
Author:Santhosh Kumar
Date Created: 16/01/24
Date Modified:
"""
@api.post("newOrderByOrd",response=OrderOut)
def newOrderByOrder(request,data:OrderIn):
    order=Order()
    result=dictToEnt(data.__dict__,order)
    book = requests.get("http://localhost:8003/api/getByCode/" + data.bookCode).json()
    result.price=book['price']
    result.total=(result.quantity *result.price)+(book['rating']*10)
    result.status=1
    result.dateOrd=datetime.date.today()
    result.save()
    deleteIndividual(request,data.customerCode,data.bookCode)
    return result

"""
Getting order by customer code
param:Customer Code
Author: Santhosh Kumar
Date Created: 16/01/24
Date Modified:
"""
@api.get("getOrdByCusCode/{cusCode}",response=List[OrderOut])
def getOrderByCusCode(request,cusCode:str):
    data=Order.objects.filter(customerCode=cusCode).values()
    result=list(map(lambda b: dictToEnt(b,Order()),data))
    return result







