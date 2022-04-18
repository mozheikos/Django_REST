import React from "react";
import {Link} from "react-router-dom";

const LoginButton = ({user, App}) => {
    if (user) {
        return (
            <div className={"login_box"}>
                <span className={"username"}> Welcome, <b>{user.firstName}</b></span>
                <Link to={"/"} className={"logout"} onClick={(event) => {
                    event.preventDefault();
                    App.logout();
                }}>Log out</Link>
            </div>
        )
    }
    return (
        <div className={"login_box"}>
            <Link className={"logout"} to={"/login"}>Log in</Link>
        </div>
    )
}
export default LoginButton;