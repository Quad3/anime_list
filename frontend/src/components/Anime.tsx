import React from 'react';

import {AnimeResponse} from "../models/AnimeResponse";

const Anime = ({ anime } : {anime : AnimeResponse}) => {
    return (
        <div className="anime" key={anime.uuid}>
            <strong>{anime.name}</strong>
            <p>{anime.state}</p>
            <p>{anime.rate}</p>
            <ol>
                {anime.start_end.map(item => (
                    <li key={item.start_date + item.end_date}>{item.start_date} - {item.end_date}</li>
                ))}
            </ol>
        </div>
    );
};

export default Anime;
