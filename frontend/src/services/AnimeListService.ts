import {AxiosResponse} from "axios";

import $api from "../http";
import {AnimeResponse, AnimeCreate, PaginatedAnimeResponse} from "../models/Anime";

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

    static async getById(uuid: string): Promise<AxiosResponse<AnimeResponse>> {
        return $api.get<AnimeResponse>(
            `/anime/${uuid}`,
        );
    }
}
