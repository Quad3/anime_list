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

    async login(username: string, password: string) {
        try {
            const response = await AuthService.login(username, password);
            localStorage.setItem('token', response.data.access_token);
            this.setIsAuth(true);
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        }
    }

    async signup(username: string, password: string) {
        try {
            const response = await AuthService.signup(username, password);
            await this.login(username, password);
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
