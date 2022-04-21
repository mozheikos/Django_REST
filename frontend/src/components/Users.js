import React from 'react';
import {Link} from "react-router-dom";

const User = ({user}) => {
    return (
        <tr className="row">
            <td className="column">
                <Link className={"list_link"} to={`/users/${user.id}`}><span>{user.username}</span></Link>
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

const UsersList = ({App, users}) => {
    let start = (App.state.users_page - 1) * App.state.users_limit;
    let end = start + App.state.users_limit;
    users = users.slice(start, end)
    return (
            <div>
                <div className={"paginator_box"}>
                    <button className={"button"} onClick={() => {
                        let page = App.state.users_page;
                        if (page > 1) {
                            App.setState({
                                "users_page": page - 1,
                            });
                        }
                    }}>Previous</button>
                    <span className={"paginator"}>Page: {App.state.users_page} of {App.state.users_pages}</span>
                    <button className={"button"} onClick={() => {
                        let page = App.state.users_page;
                        let pages = App.state.users_pages;
                        let offset = App.state.users_offset;
                        let limit = App.state.users_limit;
                        if (page < pages) {
                            App.setState({
                                "users_page": page + 1
                            })
                            if (page + 1 > (offset + limit) / limit ) {
                                App.setState({
                                    "users_offset": offset + limit
                                })
                            }
                        }
                    }}>Next</button>
                </div>
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
        </div>
    );
};

export default UsersList;