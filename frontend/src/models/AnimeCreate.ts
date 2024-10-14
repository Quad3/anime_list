import {StartEnd} from "./StartEnd";

export interface AnimeCreate {
    name: string;
    rate: number;
    review: string;
    start_end: StartEnd[];
}
