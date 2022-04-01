import React from "react";

const Remark = ({remark}) => {
    return (
        <tr className="row">
            <td className="column">
                <span>{remark.user}</span>
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
        </tr>
    );
}

const Remarks = ({remarks}) => {
    return (
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
            {remarks.map((remark) => <Remark key={remark.id} remark={remark}/>)}
        </table>
    );
}
export default Remarks;