import React from "react";
import {Link} from "react-router-dom";

const LoginButton = ({user, App}) => {
    if (user) {
        return (
            <div className={"login_box"}>
                <span className={"username"}> Welcome, <b>{user.firstName}</b></span>
                <button className={"logout"} onClick={() => {
                    App.logout();
                }}>LOGOUT</button>
            </div>
        )
    }
    return (
        <div className={"login_box"}>
            <Link className={"logout"} to={"/login"}>LOGIN</Link>
        </div>
    )
}
export default LoginButton;