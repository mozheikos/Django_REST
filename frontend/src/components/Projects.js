import React from "react";

const Project = ({project}) => {
    return (
        <tr className="row">
            <td className="column">
                <span>{project.title}</span>
            </td>
            <td className="column">
                <span>{project.url}</span>
            </td>
            <td className="column">
                <span>{project.repositoryLink}</span>
            </td>
            <td className="column">
                <span>{project.users}</span>
            </td>
        </tr>
    );
}

const Projects = ({projects}) => {
    return (
        <table className='inner_table container'>
            <th className="column">
                <span>Title</span>
            </th>
            <th className="column">
                <span>Url</span>
            </th>
            <th className="column">
                <span>Repository Link</span>
            </th>
            <th className="column">
                <span>Users</span>
            </th>
            {projects.map((project) => <Project project={project}/>)}
        </table>
    );
}
export default Projects;