import {AxiosResponse} from "axios";

import $api from "../http";
import {PaginatedAnimeResponse} from "../models/PaginatedAnimeResponse";

export default class AnimeListService {
    static async getAll(): Promise<AxiosResponse<PaginatedAnimeResponse>> {
        return $api.get<PaginatedAnimeResponse>("/anime")
    }
}
