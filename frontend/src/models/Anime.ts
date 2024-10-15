export interface PaginatedAnimeResponse {
    data: AnimeResponse[];
    count: number;
}

export interface AnimeResponse {
    name: string;
    state: string;
    rate: number;
    review: string;
    start_end: StartEnd[];
    user_id: string;
    uuid: string;
}

export interface AnimeCreate {
    name: string;
    rate: number;
    review: string;
    start_end: StartEnd[];
}

interface StartEnd {
    start_date: string;
    end_date: string;
}
