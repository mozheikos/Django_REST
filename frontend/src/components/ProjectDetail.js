import React from "react";
import {Link, useParams} from "react-router-dom";

const ProjectUser = ({ user }) => {
    return (
        <div>
            {<Link to={`/users/${user.id}`}>{user.username}</Link>}
        </div>
    )
}


const ProjectDetail = ({projects, users}) => {
    let { id } = useParams();
    id = Number.parseInt(id);
    let project = projects.find(item => item.id === id);
    if (!projects.length || !users.length) {
        return (
            <table className='inner_table container'>
                <tr><td><h1>Идет загрузка....</h1></td></tr>
            </table>
        )
    }
    return (
        <table className='inner_table container'>
            <tr>
                <td><b>Title: </b></td>
                <td>{project.title}</td>
            </tr>
            <tr>
                <td><b>Repository Link: </b></td>
                <td>{project.repositoryLink}</td>
            </tr>
            <tr>
                <td><b>Users: </b></td>
                <td>
                    {project.users.map((user) => <ProjectUser user={users.find(item => item.id === user)}/>)}
                </td>
            </tr>
        </table>
    );
}
export default ProjectDetail;