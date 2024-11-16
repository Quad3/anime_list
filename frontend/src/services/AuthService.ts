import {AxiosResponse} from 'axios';

import $api from '../http';
import {AuthResponse, SignupResponse, Message} from "../models/Auth";

export default class AuthService {
    static async login(username: string, password: string): Promise<AxiosResponse<AuthResponse>> {
        return $api.post<AuthResponse>(
            '/users/access-token',
            {username, password},
            {headers: {"Content-Type": "multipart/form-data"}},
        )
    }

    static async signup(username: string, password: string): Promise<AxiosResponse<SignupResponse>> {
        return $api.post<SignupResponse>(
            '/users/signup',
            {username, password},
        )
    }

    static async recoverPassword(email: string): Promise<AxiosResponse<Message>> {
        return $api.post<Message>(`/users/password-recovery/${email}`)
    }

    static async resetPassword(resetToken: string | null, newPassword: string): Promise<AxiosResponse<Message>> {
        return $api.post<Message>(
            '/users/reset-password',
            {token: resetToken, new_password: newPassword},
        );
    }
}
