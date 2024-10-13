import {StartEnd} from "./StartEnd";

export interface AnimeResponse {
    name: string;
    state: string;
    rate: number;
    review: string;
    start_end: StartEnd[];
    user_id: string;
    uuid: string;
}
