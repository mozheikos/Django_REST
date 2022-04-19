import React from "react";
import axios from "axios";

class ToDOCreate extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            'projects': [],
        }
    }

    componentDidMount() {
        const url = `http://127.0.0.1:8000/api/projects/?title=&users=${this.props.user.id}`
        axios.get(url
            ).then(
                response => {
                    this.setState({
                        'projects': response.data.results
                    })
                }
        ).catch(
            error => console.log(error)
        )
    }

    handleSubmit(event) {
        event.preventDefault();
        const form = event.target;
        const data = {"user": this.props.user.id, "project": null, "text": null,}
        for (let item of form.children) {
            if (item.name === "text"){
                data[item.name] = item.value
            } else if (item.name === "project"){
                // data[item.name] = this.state.projects.filter(project => project.id === +item.value)[0]
                data[item.name] = this.state.projects.filter(project => project.id === +item.value)[0].id
            }
        }
        this.props.get_new_remark(data);
    }

    render() {
        return (
            <form id={"createRemark"} onSubmit={(event) => this.handleSubmit(event)}>
                <select name={"project"} >
                    {this.state.projects.map(
                        (project) => <option key={project.id} value={project.id}>{project.title}</option>)}
                </select>
                <textarea name={"text"} placeholder={"input text"} />
                <button type={"submit"} form={"createRemark"}>Create</button>
            </form>
        )
    }
}

export default ToDOCreate;