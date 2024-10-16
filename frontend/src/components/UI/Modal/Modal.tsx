import React from 'react';

import cl from './Modal.module.css';

type propsType = {
    children: React.ReactNode,
    visible: boolean,
    setVisible: React.Dispatch<boolean>,
}

const Modal = ({children, visible, setVisible}: propsType) => {
    const rootClasses = [cl.modal]
    if (visible)
        rootClasses.push(cl.active)

    return (
        <div className={rootClasses.join(' ')} onClick={() => setVisible(false)}>
            <div className={cl.modalContent} onClick={(e) => e.stopPropagation()}>
                {children}
            </div>
        </div>
    );
};

export default Modal;
