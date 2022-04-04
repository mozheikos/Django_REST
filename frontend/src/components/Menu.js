import React from 'react';
import {NavLink} from "react-router-dom";

const MenuLink = ({link, path}) => {
    return (
        <li>
            <NavLink to={path} className="menu_link">{link}</NavLink>
        </li>
    );
};

const Menu = ({links}) => {
    return (
        <nav>
            <ul className="footer_info container">
                    {links.map((link, index) => < MenuLink key={index} link={link.verbose_name} path={link.link}/>)}
            </ul>
        </nav>
    );
};
export default Menu;