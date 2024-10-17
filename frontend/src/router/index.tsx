import React from "react";
import {Navigate, createBrowserRouter, Outlet} from "react-router-dom";

import AnimeList from "../components/AnimeList";
import LoginForm from "../components/UI/AuthForms/LoginForm";
import CreateAnimeForm from "../components/CreateAnimeForm";
import Navbar from "../components/Navbar";
import AnimeDetail from "../components/AnimeDetail";
import SignupForm from "../components/UI/AuthForms/SIgnupForm";

const _privateRoutes = [
    {
        path: '/anime',
        element: <AnimeList/>,
    },
    {
        path: '/anime/:uuid',
        element: <AnimeDetail/>,
    },
    {
        path: '/create',
        element: <CreateAnimeForm/>,
    },
    {
        path: '*',
        element: <Navigate to={'/anime'}/>,
    },
];

export const _publicRoutes = [
    {
        path: '/login',
        element: <LoginForm/>,
    },
    {
        path: '/signup',
        element: <SignupForm/>,
    },
    {
        path: '*',
        element: <Navigate to={'/login'}/>,
    },
];

export const privateRoutes = createBrowserRouter([
    {
        path: '/',
        element: <NavbarWrapper/>,
        children: _privateRoutes,
    }
]);

export const publicRoutes = createBrowserRouter([
    {
        path: '/',
        element: <NavbarWrapper/>,
        children: _publicRoutes,
    }
]);

function NavbarWrapper() {
    return (
        <div>
            <Navbar/>
            <Outlet/>
        </div>
    )
}
