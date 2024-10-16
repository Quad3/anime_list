import React, {useEffect, useState} from 'react';
import {useParams} from "react-router-dom";

import {AnimeResponse} from "../models/Anime";
import AnimeListService from "../services/AnimeListService";

const AnimeDetail = () => {
    const { uuid = '' } = useParams<{uuid: string}>();
    const [anime, setAnime] = useState<Partial<AnimeResponse>>({});
    const [isAnimeListLoading, setIsAnimeListLoading] = useState<boolean>(false);

    useEffect(() => {
        fetchAnime()
    }, [])

    async function fetchAnime() {
        setIsAnimeListLoading(true);
        try {
            const response = await AnimeListService.getById(uuid);
            setAnime(response.data);
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        } finally {
            setIsAnimeListLoading(false);
        }
    }

    return (
        <main>
            {isAnimeListLoading
                ?
                <h1>Идет загрузка</h1>
                :
                <>
                    <h2>{anime.name}</h2>
                    <p>{anime.state}</p>
                    <p>{anime.rate}</p>
                    <ol>
                        {anime.start_end?.map(item => (
                            <li key={item.start_date + item.end_date}>{item.start_date} - {item.end_date}</li>
                        ))}
                    </ol>
                </>
            }
        </main>
    );
};

export default AnimeDetail;
