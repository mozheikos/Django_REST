import React from 'react';

const User = ({user}) => {
    return (
        <tr class="row">
            <td class="column">
                <span>{user.username}</span>
            </td>
            <td class="column">
                <span>{user.first_name}</span>
            </td>
            <td class="column">
                <span>{user.last_name}</span>
            </td>
            <td class="column">
                <span>{user.email}</span>
            </td>
        </tr>
    );
};

const UsersList = ({users}) => {
    return (
        <table class='inner_table container'>
            <th class="column">
                <span>Username</span>
            </th>
            <th class="column">
                <span>First Name</span>
            </th>
            <th class="column">
                <span>Last Name</span>
            </th>
            <th class="column">
                <span>E-mail address</span>
            </th>
            {users.map((user) => <User user={user}/>)}
        </table>
    );
};

export default UsersList;