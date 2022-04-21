import React from "react";

const ToDOCreate = ({App}) => {
    if (!App.state.user){
        return (<h1>Идет загрузка...</h1>)
    }
    let projects = App.state.projects.filter(project => project.users.includes(App.state.user.id))
    return (
        <form id={"createRemark"} onSubmit={(event) => {
            const data = {"user": App.state.user.id, "project": null, "text": null,}
            for (let item of event.target.children) {
                if (item.name === "text"){
                    data[item.name] = item.value
                } else if (item.name === "project"){
                    data[item.name] = item.value
                }
            }
            App.create_remark(data)
        }}>
            <label>Remark:</label>
            <textarea className={"formInput"} name={"text"} placeholder={"input text"} />
            <label>For project:</label>
            <select className={"formSingleSelect"} name={"project"} >
                {projects.map(
                    (project) => <option key={project.id} value={project.id}>{project.title}</option>)}
            </select>
            <button className={"button"} type={"submit"} form={"createRemark"}>Create</button>
        </form>
    )
}

export default ToDOCreate;