import React from "react";

class LoginComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    handlerSubmit (event) {
        event.preventDefault()
        let cred = {'username': '', 'password': ''};
        for (let input of event.target.children) {
            if (input.tagName === "INPUT") {
                cred[input.name] = input.value
            }
        }
        this.props.get_token(cred.username, cred.password);
    }

    render() {
        return (
                <form id={"login"} onSubmit={(event) => this.handlerSubmit(event)}>
                    <label className={"label"}>Username: </label>
                    <input className={"input"} type={"text"} name={"username"} placeholder={"Enter username"}/>
                    <label className={"label"}>Password: </label>
                    <input className={"input"} type={"password"} name={"password"} placeholder={"Enter password"}/>
                    <button className={'logout login'} type={'submit'} form={"login"}>Login</button>
                </form>
        )
    }
}

export default LoginComponent;