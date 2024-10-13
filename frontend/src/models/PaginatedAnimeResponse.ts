import {AnimeResponse} from "./AnimeResponse";

export interface PaginatedAnimeResponse {
    data: AnimeResponse[];
    count: number;
}
