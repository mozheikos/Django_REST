import React from "react";
import {useParams} from "react-router-dom";

const UserProject = ({project}) => {
    return (
        <div>{project.title}</div>
    )
}


const UserDetail = ({users, projects}) => {
    let { id } = useParams();
    id = Number.parseInt(id);
    if (!projects.length || !users.length) {
        return (
            <table className='inner_table container'>
                <tr><td><h1>Идет загрузка....</h1></td></tr>
            </table>
        )
    }
    let user = users.find(user => user.id === id);
    let superUser = user.isSuperuser ? "yes" : "no";
    return (
        <table className='inner_table container'>
            <tr>
                <td><b>UserName: </b></td>
                <td>{user.username}</td>
            </tr>
            <tr>
                <td><b>First Name: </b></td>
                <td>{user.firstName}</td>
            </tr>
            <tr>
                <td><b>Last Name: </b></td>
                <td>{user.lastName}</td>
            </tr>
            <tr>
                <td><b>E-Mail address: </b></td>
                <td>{user.email}</td>
            </tr>
            <tr>
                <td><b>Is Superuser: </b></td>
                <td>{superUser}</td>
            </tr>
            <tr>
                <td><b>Projects: </b></td>
                <td>
                    {user.projectSet.map((project) => <UserProject project={project}/>)}
                </td>
            </tr>
        </table>
    )
}

export default UserDetail;