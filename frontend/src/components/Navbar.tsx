import React, {useContext} from 'react';

import {Context} from "../index";
import '../styles/navbar.css';

const Navbar = () => {
    const {store} = useContext(Context);

    function logout() {
        localStorage.removeItem('token');
        store.setIsAuth(false);
    }

    return (
        <nav className="main-navbar">
            <ul>
                <div className="nav-items">
                    <li><a href="/anime">Anime list</a></li>
                    <li><a href="/create">Create</a></li>
                </div>
                { store.isAuth
                    ?
                    <li onClick={ logout }>Выйти</li>
                    :
                    <></>
                }
            </ul>
        </nav>
    );
};

export default Navbar;
