import React, {useContext, useState} from 'react';
import {observer} from "mobx-react-lite";
import {Link} from "react-router-dom"

import {Context} from "../../../index";
import cl from './Auth.module.css';

const LoginForm = () => {
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const {store} = useContext(Context)

    return (
        <main className={cl.mainAuth}>
            <h2>Войти</h2>
            <input
                onChange={e => setEmail(e.target.value)}
                value={email}
                type="text"
                placeholder="Введите эл. почту"
            />
            <input
                onChange={e => setPassword(e.target.value)}
                value={password}
                type="password"
                placeholder="Введите пароль"
            />
            <Link to="/password-recovery">Забыли пароль?</Link>
            <button onClick={() => store.login(email, password)}>Войти</button>
        </main>
    );
};

export default observer(LoginForm);
