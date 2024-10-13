import axios from 'axios';

export const API_URL = 'http://localhost:5000/api/v1';

const $api = axios.create({
    withCredentials: true,
    baseURL: API_URL,
})

$api.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
    return config
})

$api.interceptors.response.use((config) => {
    return config;
}, (error => {
    const originalRequest = error.config;
    if (error.config && error.config._isRetry) {
        throw error;
    }
    if (error.response.status === 403 && localStorage.getItem('token')) {
        localStorage.removeItem('token');
    }
    originalRequest._isRetry = true;
    return $api.request(originalRequest);
}))

export default $api;
