import React, {useContext, useState} from 'react';
import {observer} from "mobx-react-lite";

import {Context} from "../../../index";
import cl from './Auth.module.css';

const SignupForm = () => {
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [password2, setPassword2] = useState<string>('');
    const {store} = useContext(Context)

    async function validateAndSignup() {
        if (password !== password2)
            return
        await store.signup(email, password);
    }

    return (
        <main className={cl.mainAuth}>
            <h2>Регистрация</h2>
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
            <input
                onChange={e => setPassword2(e.target.value)}
                value={password2}
                type="password"
                placeholder="Повторите пароль"
            />
            <button onClick={validateAndSignup}>Зарегистрироваться</button>
        </main>
    );
};

export default observer(SignupForm);
