import React from "react";
import { Link } from "react-router-dom";

function Header() {
  return (
    <nav
      className="navbar navbar-expand-lg navbar-light bg-light"
      style={{ backgroundColor: "#e3f2fd" }}
    >
      <Link className="navbar-brand" to={"/"}>
        Navbar
      </Link>
      <button
        className="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon"></span>
      </button>

      <div className="collapse navbar-collapse" id="navbarSupportedContent">
        <ul className="navbar-nav mr-auto">
          <li className="nav-item active">
            {/* <a className="nav-link" href="#">
              Home
            </a> */}
            <Link className="nav-link" to={"/"}>
              Admin Page
            </Link>
          </li>
          <li className="nav-item active">
            <Link className="nav-link" to={"/orders"}>
              User Page
            </Link>
          </li>
          {/* <li className="nav-item active">
            <Link className="nav-link" to={"/contact"}>
              Contact
            </Link>
          </li>
          <li className="nav-item active">
            <Link className="nav-link" to={"/alert"}>
              Alert Page
            </Link>
          </li>
          <li className="nav-item active">
            <Link className="nav-link" to={"/danger"}>
              Danger Page
            </Link>
          </li> */}
        </ul>
      </div>

      <form className="form-inline my-2 my-lg-0">
        <input
          className="form-control mr-sm-2"
          type="search"
          placeholder="Search"
          aria-label="Search"
        />
      </form>
    </nav>
  );
}

export default Header;
