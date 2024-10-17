import React, {useContext} from 'react';
import {Link} from "react-router-dom";

import {Context} from "../index";
import '../styles/navbar.css';
import logo from '../assets/logo.jpg';

const Navbar = () => {
    const {store} = useContext(Context);

    function logout() {
        localStorage.removeItem('token');
        store.setIsAuth(false);
    }

    return (
        <nav className="main-navbar">
            <ul>
                <li><Link to="/anime"><img className="nav-logo" src={logo} alt="My Anime List"/></Link></li>
                { store.isAuth
                    ?
                    <>
                        <div className="nav-items">
                            <li><Link to="/anime">Список Аниме</Link></li>
                            <li><Link to="/create">Создать</Link></li>
                        </div>
                        <div className="auth-btns">
                            <li id="logout-btn" onClick={ logout }><Link to="/login">Выйти</Link></li>
                        </div>
                    </>
                    :
                    <div className="auth-btns">
                        <li id="signup-btn"><Link to="/signup">Регистрация</Link></li>
                        <li id="login-btn"><Link to="/login">Войти</Link></li>
                    </div>
                }
            </ul>
        </nav>
    );
};

export default Navbar;
