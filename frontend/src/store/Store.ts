import {makeAutoObservable} from 'mobx';

import AuthService from "../services/AuthService";

export default class Store {
    isAuth = false;

    constructor() {
        makeAutoObservable(this);
    }

    setIsAuth(bool: boolean) {
        this.isAuth = bool;
    }

    async login(username: string, password: string) {
        try {
            const response = await AuthService.login(username, password);
            localStorage.setItem('token', response.data.access_token);
            this.setIsAuth(true);
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        }
    }

    // TODO signup
    // async signup(username: string, password: string) {}
}
