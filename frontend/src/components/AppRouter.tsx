import React, {useContext} from 'react';
import {RouterProvider} from 'react-router-dom';
import {observer} from "mobx-react-lite";

import {privateRoutes, publicRoutes} from "../router";
import {Context} from "../index";

const AppRouter = () => {
    const {store} = useContext(Context);

    return (
        <div>
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
