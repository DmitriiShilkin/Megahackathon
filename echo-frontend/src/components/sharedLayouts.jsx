import {Link, Outlet} from 'react-router-dom';
import SharedLayout from './sharedLayout';

const SharedLayouts = () => {
    return (
        <>
        <SharedLayout />
        <Outlet />
        </>
    )
}

export default SharedLayouts