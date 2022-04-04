import React from "react";
import {Link} from "react-router-dom";


const Project = ({project, users}) => {
    let users_list = users.filter((user) => project.users.includes(user.id));
    return (
        <tr className="row">
            <td className="column">
               <Link className={"list_link"} to={`/projects/${project.id}`}>{project.title}</Link>
            </td>
            <td className="column">
                <span>{project.repositoryLink}</span>
            </td>
            <td className="column">
                {users_list.map((user) => <div key={user.id}>{user.username}</div>)}
            </td>
        </tr>
    );
}

const Projects = ({App, projects, users}) => {
    let start = (App.state.projects_page - 1) * 10;
    let end = start + 10;
    projects = projects.slice(start, end);
    return (
        <div>
            <div className={"paginator_box"}>
                <button onClick={() => {
                    let page = App.state.projects_page;
                    if (page > 1) {
                        App.setState({
                            "projects_page": page - 1,
                        });
                    }
                }}>Previous</button>
                <span className={"paginator"}>Page: {App.state.projects_page} of {App.state.projects_pages}</span>
                <button onClick={() => {
                    let page = App.state.projects_page;
                    let pages = App.state.projects_pages;
                    let offset = App.state.projects_offset;
                    let limit = App.state.projects_limit;
                    if (page < pages) {
                        App.setState({
                            "projects_page": page + 1
                        })
                        if (page + 1 > (offset + limit) / limit ) {
                            App.setState({
                                "projects_offset": offset + limit
                            })
                        }
                    }
                }}>Next</button>
            </div>
            <table className='inner_table container'>
                <th className="column">
                    <span>Title</span>
                </th>
                <th className="column">
                    <span>Repository Link</span>
                </th>
                <th className="column">
                    <span>Users</span>
                </th>
                {projects.map((project) => <Project key={project.id} project={project} users={users}/>)}
            </table>
        </div>
);
}
export default Projects;