import React, {useEffect, useState} from 'react';
import {observer} from "mobx-react-lite";

import Anime from "./Anime";
import {AnimeResponse} from "../models/AnimeResponse";
import AnimeListService from "../services/AnimeListService";

const AnimeList = () => {
    const [animeList, setAnimeList] = useState<AnimeResponse[]>([]);
    const [isAnimeListLoading, setIsAnimeListLoading] = useState<boolean>(false);

    useEffect(() => {
        fetchAnimeList();
    }, []);

    async function fetchAnimeList() {
        setIsAnimeListLoading(true);
        try {
            const paginatedAnimeList = await AnimeListService.getAll();
            setAnimeList(paginatedAnimeList.data.data);
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        } finally {
            setIsAnimeListLoading(false);
        }
    }

    return (
        <div>
            {isAnimeListLoading
                ?
                <h1>Идет загрузка</h1>
                :
                <div className="anime-list">
                    {animeList.map((anime, i) => (
                        <div key={"div-" + anime.uuid}>
                            {i === 0 && <h3 key={anime.user_id}>User ID: {anime.user_id}</h3>}
                            <Anime anime={anime} key={i} />
                        </div>
                    ))}
                </div>
            }
        </div>
    );
};

export default observer(AnimeList);
