import React from "react";

const ProjectCreate = ({App}) => {
    if (!App.state.user){
        return (<h1>Идет загрузка...</h1>)
    }
    return (
        <form id={"createProject"} onSubmit={(event) => {
                event.preventDefault();
                const form = event.target;
                const data = {"title": null, "users": [], "repository_link": null}
                for (let item of form.children) {
                    if (item.name in data && item.name !== "users") {
                        data[item.name] = item.value
                    } else if (item.name === "users") {
                        for (let option of item.selectedOptions) {
                            data[item.name].push(Number.parseInt(option.value))
                        }
                    }
                }
                App.create_project(data);
            }
        }>
            <label>Title:</label>
            <input className={"formInput"} type={"text"} name={"title"} placeholder={"input title"}/>
            <label>Repository Link:</label>
            <input className={"formInput"} type={'url'} name={"repository_link"}/>
            <label>Users:</label>
            <select className={"formSelect"} name={"users"} multiple={true}>
                {App.state.users.map((user) => <option key={user.id} value={user.id}>{user.username}</option>)}
            </select>
            <button className={"button"} type={"submit"} form={"createProject"}>Create</button>
        </form>
    )

}
export default ProjectCreate;