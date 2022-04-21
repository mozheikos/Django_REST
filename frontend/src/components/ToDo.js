import React from "react";
import {Link} from "react-router-dom";

const Remark = ({App, remark, users}) => {
    let user = users.find(user => user.username === remark.user)
    return (
        <tr className="row">
            <td className="column">
                <span>{user.username}</span>
            </td>
            <td className="column">
                <span>{remark.project}</span>
            </td>
            <td className="column">
                <span>{remark.text}</span>
            </td>
            <td className="column">
                <span>{remark.status}</span>
            </td>
            {<td className="column">
                {App.is_authenticated() ? <div>
                        <button className={"button"} onClick={() => {App.delete_remark(remark.id)}}>delete remark</button>

                    </div>
                                        : <div>Login to advanced</div>}
            </td>}
        </tr>
    );
}

const Remarks = ({App, remarks, users}) => {
    if (!users.length) {
        return (
            <table className='inner_table container'>
                <tr><td><h1>Идет загрузка....</h1></td></tr>
            </table>
        )
    }
    let start = (App.state.remarks_page - 1) * App.state.remarks_limit;
    let end = start + App.state.remarks_limit;
    remarks = remarks.slice(start, end);
    return (
        <div>
            <div className={"paginator_box"}>
                <button className={"button"} onClick={() => {
                    let page = App.state.remarks_page;
                    if (page > 1) {
                        App.setState({
                            "remarks_page": page - 1,
                        });
                    }
                }}>Previous</button>
                <span className={"paginator"}>Page: {App.state.remarks_page} of {App.state.remarks_pages}</span>
                <button className={"button"} onClick={() => {
                    let page = App.state.remarks_page;
                    let pages = App.state.remarks_pages;
                    let offset = App.state.remarks_offset;
                    let limit = App.state.remarks_limit;
                    if (page < pages) {
                        App.setState({
                            "remarks_page": page + 1
                        })
                        if (page + 1 > (offset + limit) / limit ) {
                            App.setState({
                                "remarks_offset": offset + limit
                            })
                        }
                    }
                }}>Next</button>
            </div>
            <button className={"button"} ><Link to={"/ToDo/create"}>Create remark</Link></button>
            <table className='inner_table container'>
                <th className="column">
                    <span>User</span>
                </th>
                <th className="column">
                    <span>Project</span>
                </th>
                <th className="column">
                    <span>Text</span>
                </th>
                <th className="column">
                    <span>Status</span>
                </th>
                <th></th>
                {remarks.map((remark) => <Remark App={App} remark={remark} users={users}/>)}
            </table>
        </div>
    );
}
export default Remarks;