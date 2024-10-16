import React from 'react';
import {useNavigate} from 'react-router-dom';

import {AnimeResponse} from "../models/Anime";
import '../styles/main.css';

const Anime = ({ anime } : {anime : AnimeResponse}) => {
    const navigate = useNavigate();

    function getFormattedDate(s: string) {
        const date = new Date(Date.parse(s))
        return date.toLocaleDateString('ru-RU')
    }

    return (
        <div className="anime" key={anime.uuid}>
            <strong className="anime-title" onClick={() => navigate(`/anime/${anime.uuid}`)}>{anime.name}</strong>
            <p>{anime.state}</p>
            <p>{anime.rate}</p>
            <ol>
                {anime.start_end.map(item => (
                    <li key={item.start_date + item.end_date}>{getFormattedDate(item.start_date)} - {getFormattedDate(item.end_date)}</li>
                ))}
            </ol>
        </div>
    );
};

export default Anime;
