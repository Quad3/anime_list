import React, {useState} from 'react';
import {observer} from "mobx-react-lite";
import {useNavigate, useSearchParams} from "react-router-dom";

import cl from './Auth.module.css';
import AuthService from "../../../services/AuthService";

const ResetPassword = () => {
    const [searchParams] = useSearchParams();
    const resetToken: string | null = searchParams.get("token");
    const [password, setPassword] = useState<string>('');
    const [password2, setPassword2] = useState<string>('');
    const [success, setSuccess] = useState<boolean>(false);
    const navigate = useNavigate();

    async function resetPassword() {
        if (resetToken === null && password !== password2) {
            return
        }
        try {
            const response = await AuthService.resetPassword(resetToken, password);
            if (response.status === 200) {
                setSuccess(true);
                setTimeout(() => navigate("login"), 2000);
            }
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        }
    }

    return (
        <main className={cl.mainAuth}>
            <h2>Восстановление пароля</h2>
            <input
                onChange={e => setPassword(e.target.value)}
                value={password}
                type="password"
                placeholder="Введите новый пароль"
            />
            <input
                onChange={e => setPassword2(e.target.value)}
                value={password2}
                type="password"
                placeholder="Повторите новый пароль"
            />
            <button onClick={resetPassword}>Изменить пароль</button>
            {success
                ?
                <h3>Пароль изменен</h3>
                :
                <></>
            }
        </main>
    );
};

export default observer(ResetPassword);
