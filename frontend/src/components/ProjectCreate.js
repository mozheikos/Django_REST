import React from "react";
import axios from "axios";


class ProjectCreate extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            'users': [],
            'count': 0
        }
    }
    componentDidMount() {
        const url = "http://127.0.0.1:8000/api/users"
        axios.get(url
            ).then(
                response => {
                    // console.dir(response);
                    const offset = response.data.results.length;
                    const limit = response.data.count - offset;
                    this.setState({
                        "users": response.data.results,
                        "count": response.data.count
                    });
                    axios.get(url + `?offset=${offset}&limit=${limit}`).then(
                        response2 => {
                            const users = this.state.users;
                            users.push(...response2.data.results);
                            this.setState({
                                "users": users
                            })
                        }
                    )
                }
        ).catch(error => {console.log(error)})
    }

    handleSubmit(event) {
        event.preventDefault();
        const form = event.target;
        const data = {"title": null, "users": [], "repository_link": null}
        for (let item of form.children) {
            if (item.name in data && item.name !== "users"){
                data[item.name] = item.value
            } else if (item.name === "users") {
                data[item.name].push(Number.parseInt(item.value))
            }
        }
        console.dir(data);
        this.props.get_new_project(data);
    }

    render() {
        return (
            <form id={"createProject"} onSubmit={(event) => this.handleSubmit(event)}>
                <input type={"text"} name={"title"} placeholder={"input title"}/>
                <select name={"users"} onScroll={(event) => {console.dir(event)}}>
                    {this.state.users.map((user) => <option key={user.id} value={user.id}>{user.username}</option>)}
                </select>
                <input type={'url'} name={"repository_link"}/>
                <button type={"submit"} form={"createProject"}>Create</button>
            </form>
        )
    }
}

export default ProjectCreate;