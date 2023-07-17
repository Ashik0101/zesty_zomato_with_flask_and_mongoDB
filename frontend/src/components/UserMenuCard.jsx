import React from "react";
import url from "./url";
import { useState } from "react";

function MenuCard({ data }) {
  const [orderDishButtonClicked, setorderDishButtonClicked] = useState(false);
  const [quantity, setQuantity] = useState(0);

  const handleOrderDishButtonClick = (event) => {
    if (!quantity) {
      alert("Select qunatity");
      return;
    }
    let id = event.target.dataset.id;
    fetch(`${url}/orders/add/${id}`, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({ quantity, customer_name: "ashiq ansari" }),
    })
      .then((res) => res.json())
      .then((res) => {
        console.log("response after ordering :", res);
        if (res.msg == "order added!") {
          alert("Order Successfull");
        }
      })
      .catch((err) => console.log(err));
  };

  const handleQuantityChange = (event) => {
    setQuantity(event.target.value);
    console.log("quantity is :", quantity);
  };

  return (
    <div className="card" style={{ width: "14rem" }}>
      <img
        className="card-img-top"
        src={data.image}
        height={150}
        alt={data.name}
      />
      <div className="card-body">
        <h5 className="card-title">{data.dish_name}</h5>
        <p className="card-text">Price : {"Rs " + data.price}</p>
        <p className="card-text">
          {data.availability === "yes" ? "Available" : "Not Available"}
        </p>

        {orderDishButtonClicked === true ? (
          <div>
            <input
              style={{ width: "100px" }}
              type="number"
              placeholder="enter quantity..."
              required
              onChange={handleQuantityChange}
            />
            <button
              data-id={data._id}
              type="button"
              className="btn btn-warning"
              onClick={handleOrderDishButtonClick}
            >
              Place Order
            </button>{" "}
          </div>
        ) : (
          <button
            data-id={data._id}
            type="button"
            className="btn btn-danger"
            disabled={data.availability !== "yes"}
            onClick={() => {
              setorderDishButtonClicked(!orderDishButtonClicked);
            }}
          >
            Order Dish
          </button>
        )}
      </div>
    </div>
  );
}

export default MenuCard;
