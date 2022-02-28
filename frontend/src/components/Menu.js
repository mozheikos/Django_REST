import React from 'react';

const MenuLink = ({link}) => {
    return (
        <li>
            <a href={'#'} className={"menu_link"}>{link}</a>
        </li>
    );
};

const Menu = ({links}) => {
    return (
        <ul className="footer_info container">
            {links.map((link) => <MenuLink link={link}/>)}
        </ul>
    );
};
export default Menu;