import React, {useEffect, useState} from 'react';

import {AnimeResponse} from "../../../models/Anime";
import Input from '../Input/Input';
import AnimeListService from "../../../services/AnimeListService";
import {getFormattedDate} from "../../../utils";

type propsType = {
    anime: Partial<AnimeResponse>,
    setAnime: React.Dispatch<Partial<AnimeResponse>>,
    setIsCompleted: React.Dispatch<boolean>,
}

const StartEndList = ({anime, setAnime, setIsCompleted}: propsType) => {
    const [completeDate, setCompleteDate] = useState<string>('')

    useEffect(() => {
        if (typeof anime.start_end?.at(-1)?.end_date !== undefined)
            setIsCompleted(true);
    }, [])

    async function completeStartEnd() {
        if (!completeDate) {
            return
        }
        try {
            const response = await AnimeListService.updateStartEnd(anime.uuid, completeDate);
            setCompleteDate('');
            if (anime.start_end) {
                anime.start_end.pop();
                anime.start_end.push(response.data);
                setAnime(anime);
                setIsCompleted(true);
            }
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        }
    }

    return (
        <ol>
            {anime.start_end?.map((item, index) => (
                item.end_date
                    ?
                    <li key={index}>{getFormattedDate(item.start_date)} - {getFormattedDate(item.end_date)}</li>
                    :
                    <>
                        <li key={index}>{getFormattedDate(item.start_date)}</li>
                        <Input
                            onChange={(e: { target: { value: React.SetStateAction<string>; }; }) => setCompleteDate(e.target.value)}
                            value={completeDate}
                            type="date"
                        />
                        <button onClick={completeStartEnd}>Закончить просмотр</button>
                    </>
            ))}
        </ol>
    );
};

export default StartEndList;
