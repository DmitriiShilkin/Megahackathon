import { Link } from "react-router-dom";
import { useState } from "react";

const Fyp = () => {
    const isAuthenticated = false;
    const [isActive, setIsActive] = useState(1);
  const toggleActive = (index) => {
      setIsActive(index)
  } 

    return (
        <div>
            {isAuthenticated ? (
                <Link to='/' />
            ) : (
                
            <div className="fyp__container">
                 <div className="fyp__containerFeed">
                    <div className="subcontainer">
                    <Link to='/feed'>
                    <button type="button" className={isActive === 0 ? ' recsbtn active' : 'recsbtn'}
                    onClick={() => toggleActive(0)}>
                    <span>Рекомендации</span> 
                    </button>
                    </Link>
                            <button type="button" className={isActive === 1 ? 'fypbtn active' : 'fypbtn'}
                            onClick={() => toggleActive(1)}>
                            <span>Моя Лента</span>
                            </button>
                        
                    </div>
                </div>
                <div className="fyp__Auth">
                <div className="fyp__doorContainer">
                <img src="/Door (1).png" className= "fyp__door" alt="background" />
                <img src="/face.png" className="fyp__face" alt="face" />
                <div className="logIn">
                    <p className="explanation">Чтобы просматривать ленту своих подписок, необходимо авторизоваться</p>
                    <button type="button" className="fyp__logInBtn"><span>Войти</span></button>
                    <button type="button" className="fyp__VKbtn"><span>VK ID</span></button>
                </div>
                </div>
                <div className="signUp">
                    <span>Ты еще не с нами?</span>
                    <button type="button"><span>Регистрация</span></button>
                </div>

                </div>
            </div>
                            )}
        </div>

    )
}

export default Fyp