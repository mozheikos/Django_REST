import React from 'react';
import {Link} from "react-router-dom";

const MenuLink = ({link, path}) => {
    return (
        <li>
            <Link to={path} className={"menu_link"}>{link}</Link>
        </li>
    );
};

const Menu = ({links}) => {
    return (
        <ul className="footer_info container">
                {links.map((link) => < MenuLink link={link.verbose_name} path={link.link}/>)}
        </ul>
    );
};
export default Menu;