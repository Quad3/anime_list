import React from "react";
import {Navigate, createBrowserRouter} from "react-router-dom";

import AnimeList from "../components/AnimeList";
import LoginForm from "../components/LoginForm";
import CreateAnimeForm from "../components/CreateAnimeForm";

export const privateRoutes = createBrowserRouter([
    {
        path: '/anime',
        element: <AnimeList/>,
    },
    {
        path: '/create',
        element: <CreateAnimeForm/>,
    },
    {
        path: '*',
        element: <Navigate to={'/anime'}/>,
    },
]);

export const publicRoutes = createBrowserRouter([
    {
        path: '/login',
        element: <LoginForm/>,
    },
    {
        path: '*',
        element: <Navigate to={'/login'}/>,
    },
]);
