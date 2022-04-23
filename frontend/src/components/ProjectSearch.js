import React from "react";


const ProjectSearch = ({App}) => {
    return (
        <div>
            <label htmlFor={"projectSearch"}>Find project:</label>
            <input id={"projectSearch"} type={"text"} placeholder={"search..."} />
            <button className={"button"} onClick={() => {
                let name = document.querySelector('#projectSearch').value;
                App.find_project(name);
            }}>Search</button>
            <button className={"button"} onClick={() => {
                let name = "";
                App.find_project(name);
            }}>Show all</button>
        </div>
    )
}
export default ProjectSearch;