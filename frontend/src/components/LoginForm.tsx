import React, {FC, useContext, useState} from 'react';

import {Context} from "../index";

const LoginForm: FC = () => {
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

export default LoginForm;
