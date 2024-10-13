import React, {useContext, useEffect, useState} from 'react';
import {observer} from 'mobx-react-lite';

import LoginForm from "./components/LoginForm";
import AnimeList from "./components/AnimeList";
import {Context} from "./index";
import AnimeListService from "./services/AnimeListService";
import {AnimeResponse} from "./models/AnimeResponse";

function App() {
    const [animeList, setAnimeList] = useState<AnimeResponse[]>([]);
    const {store} = useContext(Context);

    useEffect(() => {
        store.checkAuth();
        if (store.isAuth)
            getAnimeList();
    }, [store.isAuth]);

    async function getAnimeList() {
        try {
            const response = await AnimeListService.getAll();
            setAnimeList(response.data.data);
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        }
    }

    return (
        <div>
            {
                store.isAuth
                    ?
                    <AnimeList animeList={animeList} />
                    :
                    <LoginForm/>
            }
        </div>
    );
}

export default observer(App);
