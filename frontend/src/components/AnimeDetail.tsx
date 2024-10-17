import React, {useEffect, useState} from 'react';
import {useParams} from "react-router-dom";

import {AnimeResponse} from "../models/Anime";
import AnimeListService from "../services/AnimeListService";
import Input from "./UI/Input/Input";
import Modal from "./UI/Modal/Modal";
import StartEndList from "./UI/StartEndList/StartEndList";

const AnimeDetail = () => {
    const { uuid = '' } = useParams<{uuid: string}>();
    const [anime, setAnime] = useState<Partial<AnimeResponse>>({});
    const [isAnimeListLoading, setIsAnimeListLoading] = useState<boolean>(false);
    const [startDate, setStartDate] = useState<string>('');
    const [endDate, setEndDate] = useState<string>('');
    const [modal, setModal] = useState<boolean>(false);
    const [isCompletedStartEnd, setIsCompletedStartEnd] = useState<boolean>(false)

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

    async function createStartEnd() {
        try {
            const response = await AnimeListService.createStartEnd(anime.uuid, startDate, endDate);
            setModal(false);
            setStartDate('');
            setEndDate('');
            if (!response.data.end_date)
                setIsCompletedStartEnd(false);
            if (anime.start_end)
                anime.start_end = [...anime.start_end, response.data]
            else
                anime.start_end = [response.data]
            setAnime(anime);
        } catch (e: any) {
            console.log(e.response?.data?.detail);
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
                    <StartEndList
                        anime={anime}
                        setAnime={setAnime}
                        setIsCompleted={setIsCompletedStartEnd}
                    />
                    <button onClick={() => {setModal(true)}}>Добавить просмотр</button>

                    <Modal visible={modal} setVisible={setModal}>
                        <Input
                            onChange={(e: { target: { value: React.SetStateAction<string>; }; }) => setStartDate(e.target.value)}
                            value={startDate}
                            type="date"
                            placeholder="Введите дату начала просмотра"
                        />
                        <Input
                            onChange={(e: { target: { value: React.SetStateAction<string>; }; }) => setEndDate(e.target.value)}
                            value={endDate}
                            type="date"
                            placeholder="Введите дату окончания просмотра"
                        />
                        <button onClick={createStartEnd}>Добавить</button>
                    </Modal>
                </>
            }
        </main>
    );
};

export default AnimeDetail;
