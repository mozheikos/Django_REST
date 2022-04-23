import React from "react";
import {useParams} from "react-router-dom";


const ProjectUpdate = ({App}) => {
    let { id } = useParams();
    id = Number.parseInt(id);
    let project = App.state.projects.find(project => project.id === id);
    let users = App.state.users;
    if (!project){
        return (<h1>Идет загрузка...</h1>)
    }
    return (
        <form id={'updateProject'} onSubmit={(event) => {
            event.preventDefault();
            let form = event.target;
            let data = {
                'title': "",
                'repository_link': "",
                'users': []
            }
            for (let item of form) {
                if (item.tagName === 'INPUT'){
                    data[item.name] = item.value;

                } else if (item.tagName === 'SELECT') {
                    for (let option of item.selectedOptions) {
                        data.users.push(option.value)
                    }
                }
            }
            App.update_project(id, data);
        }}>
            <label>Title:</label>
            <input className={"formInput"} type={"text"} name={"title"} defaultValue={project.title}/>
            <label>Repository Link:</label>
            <input className={"formInput"} type={"url"} name={"repository_link"} defaultValue={project.repositoryLink} />
            <label>Users:</label>
            <select className={"formSelect"} multiple={true}>
                {users.map(user => <option selected={project.users.includes(user.id)} value={user.id}>{user.username}</option>)}
            </select>
            <button className={"button"} type={"submit"} form={"updateProject"}>Save changes</button>
        </form>
    )
}
export default ProjectUpdate;