import React, {useState} from 'react';
import {observer} from "mobx-react-lite";

import cl from './Auth.module.css';
import AuthService from "../../../services/AuthService";

const PasswordRecovery = () => {
    const [email, setEmail] = useState<string>('');
    const [success, setSuccess] = useState<boolean>(false);
    const [message, setMessage] = useState<string>('');

    async function recoverPassword() {
        try {
            const response = await AuthService.recoverPassword(email)
            if (response.status < 300) {
                setSuccess(true);
                setMessage(response.data.message);
                setTimeout(() => setSuccess(false), 3000);
            }
        } catch (e: any) {
            if (e.response?.status < 500) {
                setSuccess(true);
                setMessage(e.response?.data?.detail);
                setTimeout(() => setSuccess(false), 3000);
            }
            console.log(e.response?.data?.detail);
        }
    }

    return (
        <main className={cl.mainAuth}>
            <h2>Восстановление пароля</h2>
            <input
                onChange={e => setEmail(e.target.value)}
                value={email}
                type="text"
                placeholder="Введите эл. почту"
            />
            <button onClick={recoverPassword}>Восстановить пароль</button>
            {success
                ?
                <h3>{ message }</h3>
                :
                <></>
            }
        </main>
    );
};

export default observer(PasswordRecovery);
