import {AxiosResponse} from "axios";

import $api from "../http";
import {PaginatedAnimeResponse} from "../models/PaginatedAnimeResponse";
import {AnimeResponse} from "../models/AnimeResponse";
import {AnimeCreate} from "../models/AnimeCreate";

export default class AnimeListService {
    static async getAll(): Promise<AxiosResponse<PaginatedAnimeResponse>> {
        return $api.get<PaginatedAnimeResponse>("/anime");
    }

    static async create(animeIn: AnimeCreate): Promise<AxiosResponse<AnimeResponse>> {
        return $api.post<AnimeResponse>(
            "/anime/create",
            {...animeIn},
        );
    }
}
