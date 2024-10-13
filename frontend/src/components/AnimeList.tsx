import React from 'react'
import {observer} from "mobx-react-lite";

import Anime from "./Anime";
import {AnimeResponse} from "../models/AnimeResponse";

const AnimeList = ({ animeList } : {animeList: AnimeResponse[] }) => {
    return (
        <div className="anime-list">
            {animeList.map((anime, i) => (
                <div key={"div-" + anime.uuid}>
                    {i === 0 && <h3 key={anime.user_id}>User ID: {anime.user_id}</h3>}
                    <Anime anime={anime} key={i} />
                </div>
            ))}
        </div>
    );
};

export default observer(AnimeList);
