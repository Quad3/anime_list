import React from 'react';
import {useNavigate} from 'react-router-dom';

import {AnimeResponse} from "../models/Anime";
import '../styles/main.css';
import {getFormattedDate} from "../utils";

const Anime = ({ anime } : {anime : AnimeResponse}) => {
    const navigate = useNavigate();

    return (
        <div className="anime" key={anime.uuid}>
            <strong className="anime-title" onClick={() => navigate(`/anime/${anime.uuid}`)}>{anime.name}</strong>
            <p>{anime.state}</p>
            <p>{anime.rate}</p>
            <ol>
                {anime.start_end.map((item, index) => (
                    <li key={index}>{getFormattedDate(item.start_date)} - {getFormattedDate(item.end_date)}</li>
                ))}
            </ol>
        </div>
    );
};

export default Anime;
