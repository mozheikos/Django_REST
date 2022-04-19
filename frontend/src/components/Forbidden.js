import React from "react";
import {Link} from "react-router-dom";

const Forbidden = () => {
  return (
      <div>
          <h1>Please, authorize first</h1>
          <Link to={"/login"}>LOG IN</Link>
      </div>
  )
}
export default Forbidden;