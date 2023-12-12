import { Link } from "react-router-dom"
import PostPage from "./post"
const SharedLayout = () => {
    return (
        <div className="shared__container">
            <header>
                <div className="header">
                    <img src="/logo.svg" className="logo" alt="logo" />
                    <button type="button" className="notifBtn" 
                    >
                    <img src="/bell-inactive.svg" className="notification" alt="notification's ring"/>
                    </button>
                </div>
            </header>
            <div className="tabBar__container">
            <div className="tabBar__subcontainer">
            <Link to= 'feed'> <button type="button" className="tabBar__home"><img src="/home.svg" alt="home" /></button> </Link>
            <Link to = 'fyp'><button type="button" className="tabBar__search"><img src="/search1.svg" alt="search" /></button></Link>
            <Link to = 'creatingPost'><button type="button" className="tabBar__addPost"><img src="/add.svg" alt="add" /></button></Link>
            <button type="button" className="tabBar__favs"><img src="/favorite.svg" alt="favorites" /></button>
            <button type="button" className="tabBar__profile"><img src="/profile.svg" alt="profile" /></button>
            </div>
        </div>
        </div>
        
    )
}

export default SharedLayout