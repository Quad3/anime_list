export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export interface SignupResponse {
    username: string;
    is_active: boolean;
    is_superuser: boolean;
    uuid: string;
}

export interface Message {
    message: string;
}
