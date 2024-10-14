import React from 'react';
import {observer} from 'mobx-react-lite';

import AppRouter from "./components/AppRouter";

function App() {
    return (
        <AppRouter/>
    );
}

export default observer(App);
