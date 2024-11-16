import {makeAutoObservable} from 'mobx';

import AuthService from "../services/AuthService";

export default class Store {
    isAuth = false;

    constructor() {
        makeAutoObservable(this);
        this.checkAuth();
    }

    setIsAuth(bool: boolean) {
        this.isAuth = bool;
    }

    async login(email: string, password: string) {
        try {
            const response = await AuthService.login(email, password);
            localStorage.setItem('token', response.data.access_token);
            this.setIsAuth(true);
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        }
    }

    async signup(email: string, password: string) {
        try {
            await AuthService.signup(email, password);
            await this.login(email, password);
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        }
    }

    async checkAuth() {
        const token = localStorage.getItem('token');
        if (token && token !== "undefined") {
            this.setIsAuth(true);
        }
    }
}
