import pytest
from app import create_app


@pytest.fixture
def app():
   return create_app()

@pytest.fixture
def client(app):
   return app.test_client()


# test for get menu
def test_get_menu(client):
   response = client.get("/menu")
   assert response.status_code == 200


# test for add dish
def test_add_dish(client):

   dish = {
      'dish_name':"aalu bhurjii",
      'price':200,
      'availability':"yes",
   }
   response = client.post("/menu/add",json = dish)
   assert response.status_code == 400
   assert response.json == {"msg": "Please prived all fields!"}


   dish = {
      'dish_name':"aalu bhurjii",
      'price':200,
      'availability':"yes",
      'stock':200,
      'image':'abcd.jpg'
   }
   response = client.post("/menu/add",json = dish)
   assert response.status_code == 201
   assert response.json == {'msg':"dish added!"}


# test for update dish availability
def test_update_availability(client):
   # test with invalid objectId
   response = client.put("/menu/update/adfd445")
   assert response.status_code == 400
   assert response.json == {'msg':'Invalid ObjectId!'}

   # check with object id whose document is not present
   response = client.put("/menu/update/64a66f5815d426a3a0cc4f30")
   assert response.status_code == 404
   assert response.json == {'msg':"No document found!"}

    # check with valid object id
   obj = {
      'availability':"no",
      'stock':20495
   }
   response = client.put("/menu/update/64a66f5815d426a3a0cc4f34",json=obj)
   assert response.status_code == 200
   assert response.json ==  {'msg': 'Dish updated successfully'}


# test for delete dish
def test_delete_dish(client):
   # check for invalid id
   response = client.delete("/menu/delete/afdfd")
   assert response.status_code == 400
   assert response.json == {'msg':'Invalid ObjectId!'}

    # check with object id whose document is not present
   response = client.delete("/menu/delete/64a66f5815d426a3a0cc4f30")
   assert response.status_code == 404
   assert response.json == {'msg':"No document found!"}

   # check for valid objectId
   # response = client.delete("/menu/delete/64b44be143d6b62cc52585d0")
   # assert response.status_code == 200
   # assert response.json == {'msg': 'Dish deleted successfully'}


#************* TESTING FOR ORDERSS *************#
# test get_orders
def test_get_orders(client):
   response = client.get("/orders")
   assert response.status_code == 200

# test add_order
def test_add_order(client):
      # check for customer missing
      data = {
         'quantity':5
      }
      response = client.post("/orders/add/64a64b934f7dfaedf83de1ff",json=data)
      assert response.status_code == 400
      assert response.json == {'msg':"Customer name is missing!"}

      # check for quantity missing
      data = {
         'customer_name':'rohan'
      }
      response = client.post("/orders/add/64a64b934f7dfaedf83de1ff",json=data)
      assert response.status_code == 400
      assert response.json == {'msg':'Quantity is missing!'}

      # check for successfull order
      data = {
         'customer_name':'rohan',
         'quantity':5
      }
      response = client.post("/orders/add/64a64b934f7dfaedf83de1ff",json=data)
      assert response.status_code == 201
      assert response.json == {'msg':"order added!"}



# test update order route
def test_change_status(client):
   # check with blank status
   updates = {

   }
   response = client.put("/orders/update/64b434edef269bfc5cbf9584",json = updates)
   assert response.status_code == 400
   assert response.json == {'msg':'Please enter a status of the order!'}

   # check for invalid status
   updates = {
      'status':'anything'
   }
   response = client.put("/orders/update/64b434edef269bfc5cbf9584",json = updates)
   assert response.status_code == 400
   assert response.json == {'msg':'Please enter valid status!'}

   # check for not found
   updates = {
      'status':'preparing'
   }
   response = client.put("/orders/update/64b434edef269bfc5cbc7594",json = updates)
   assert response.status_code == 404
   assert response.json == {'msg':"No order found!"}

   # check for successful update
   updates = {
      'status':'ready for pickup'
   }
   response = client.put("/orders/update/64b434edef269bfc5cbf9584",json = updates)
   assert response.status_code == 200
   assert response.json == {'msg':'Order updated successfully!'}