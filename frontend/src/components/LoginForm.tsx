import React, {useContext, useState} from 'react';
import {observer} from "mobx-react-lite";

import {Context} from "../index";

const LoginForm = () => {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const {store} = useContext(Context)

    return (
        <div>
            <input
                onChange={e => setUsername(e.target.value)}
                value={username}
                type="text"
                placeholder="Введите имя пользователя"
            />
            <input
                onChange={e => setPassword(e.target.value)}
                value={password}
                type="password"
                placeholder="Введите пароль"
            />
            <button onClick={() => store.login(username, password)}>Логин</button>
        </div>
    );
};

export default observer(LoginForm);
