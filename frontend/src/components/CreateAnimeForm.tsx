import React, {useState} from 'react';
import {observer} from "mobx-react-lite";

import "../styles/create-anime-form.css";
import "../styles/main.css";
import AnimeListService from "../services/AnimeListService";
import Input from "./UI/Input/Input";

const CreateAnimeForm = () => {
    const [name, setName] = useState<string>('');
    const [rate, setRate] = useState<number>(1);
    const [review, setReview] = useState<string>('');
    const [startDate, setStartDate] = useState<string>('');
    const [endDate, setEndDate] = useState<string>('');

    async function createAnime() {
        try {
            const anime = await AnimeListService.create({
                name: name,
                rate: rate,
                review: review,
                start_end: [{
                    start_date: startDate,
                    end_date: endDate,
                }],
            })
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        }
    }

    return (
        <main className="create-anime-form">
            <input
                onChange={e => setName(e.target.value)}
                value={name}
                type="text"
                placeholder="Введите название аниме"
            />
            <input
                onChange={e => setRate(Number(e.target.value))}
                value={rate}
                type="number"
                placeholder="Введите оценку от 1 до 10"
            />
            <input
                onChange={e => setReview(e.target.value)}
                value={review}
                type="text"
                placeholder="Введите описание"
            />
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
            <button onClick={createAnime}>Создать</button>
        </main>
    );
};

export default observer(CreateAnimeForm);
