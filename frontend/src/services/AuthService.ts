import {AxiosResponse} from 'axios';

import $api from '../http';
import {AuthResponse} from "../models/AuthResponse";
import {SignupResponse} from "../models/SignupResponse";

export default class AuthService {
    static async login(username: string, password: string): Promise<AxiosResponse<AuthResponse>> {
        return $api.post(
            '/users/access-token',
            {username, password},
            {headers: {"Content-Type": "multipart/form-data"}},
        )
    }

    static async signup(username: string, password: string): Promise<AxiosResponse<SignupResponse>> {
        return $api.post(
            '/users/signup',
            {username, password},
        )
    }
}
