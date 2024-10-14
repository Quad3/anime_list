import React, {useContext} from 'react';
import {RouterProvider} from 'react-router-dom';
import {observer} from "mobx-react-lite";

import {privateRoutes, publicRoutes} from "../router";
import {Context} from "../index";
import Navbar from "./Navbar";

const AppRouter = () => {
    const {store} = useContext(Context);

    return (
        <div>
            <Navbar />
            { store.isAuth
                ?
                <RouterProvider router={privateRoutes}/>
                :
                <RouterProvider router={publicRoutes}/>
            }
        </div>
    );
};

export default observer(AppRouter);
