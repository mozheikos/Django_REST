import React from 'react';

const User = ({user}) => {
    return (
        <tr className="row">
            <td className="column">
                <span>{user.username}</span>
            </td>
            <td className="column">
                <span>{user.firstName}</span>
            </td>
            <td className="column">
                <span>{user.lastName}</span>
            </td>
            <td className="column">
                <span>{user.email}</span>
            </td>
        </tr>
    );
};

const UsersList = ({users}) => {
    return (
        <table className='inner_table container'>
            <th className="column">
                <span>Username</span>
            </th>
            <th className="column">
                <span>First Name</span>
            </th>
            <th className="column">
                <span>Last Name</span>
            </th>
            <th className="column">
                <span>E-mail address</span>
            </th>
            {users.map((user) => <User key={user.id} user={user}/>)}
        </table>
    );
};

export default UsersList;