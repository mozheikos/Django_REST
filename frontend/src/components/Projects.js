import React from "react";
import {Link} from "react-router-dom";



const Project = ({project, users}) => {
    let users_list = users.filter((user) => project.users.includes(user.id));
    return (
        <tr className="row">
            <td className="column">
               <Link to={`/projects/${project.id}`}>{project.title}</Link>
            </td>
            <td className="column">
                <span>{project.repositoryLink}</span>
            </td>
            <td className="column">
                {users_list.map((user) => <div key={user.id}><Link to={`/users/${user.id}`}>{user.username}</Link></div>)}
            </td>
        </tr>
    );
}

const Projects = ({projects, users}) => {
    return (
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
);
}
export default Projects;