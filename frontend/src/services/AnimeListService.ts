import {AxiosResponse} from "axios";

import $api from "../http";
import {
    AnimeResponse,
    AnimeCreate,
    PaginatedAnimeResponse,
    StartEnd,
} from "../models/Anime";
import {StartEndListResponse} from "../components/UI/Gantt/Models";

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

    static async createStartEnd(
        uuid: string | undefined,
        startDate: string,
        endDate: string,
    ): Promise<AxiosResponse<StartEnd>> {
        let data;
        if (endDate)
            data = {
                start_date: startDate,
                end_date: endDate,
            }
        else
            data = {
                start_date: startDate,
            }
        return $api.post<StartEnd>(
            `/anime/${uuid}/create-start-end`,
            {...data},
        );
    }

    static async updateStartEnd(
        uuid: string | undefined,
        endDate: string,
    ): Promise<AxiosResponse<StartEnd>> {
        return $api.patch<StartEnd>(
            `/anime/${uuid}/update-start-end`,
            {end_date: endDate},
        )
    }

    static async getStartEndList(): Promise<AxiosResponse<StartEndListResponse[]>> {
        return $api.get<StartEndListResponse[]>('/anime/start-end-list');
    }
}
