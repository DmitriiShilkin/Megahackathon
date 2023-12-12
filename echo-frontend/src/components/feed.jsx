import { Link } from 'react-router-dom';
import { useState } from 'react';
import Post from './post';

const Feed = () => {

     //меняем класс "active" при нажатии
  const [isActive, setIsActive] = useState(0);
  const toggleActive = (index) => {
      setIsActive(index)
  } 

  //дропдаун
  const [dropdown, setDropdown] =  useState(false);

  //посты
  const [posts, setPosts] = useState([
    {
      author: 'nickk',
      published: '12/12/12',
      headline: 'title',
      raiting: '*****',
      image: 'imgs',
      description: 'description',
      likes: '2',
      comments:'2'
      
    }
  ])

  return (
    <div className="wrapper">
                  
            <main>
                <div className="feed">
                <div className="container__feed">
                    <div className="subcontainer">
                    <button type="button" className={isActive === 0 ? ' recs active' : 'recs'}
                    onClick={() => toggleActive(0)}>
                    <span>Рекомендации</span> 
                    </button>
                        <Link to = 'fyp'> 
                        <button type="button" className={isActive === 1 ? 'fyp active' : 'fyp'}
                        onClick={() => toggleActive(1)}>
                        <span>Моя Лента</span>
                        </button>
                        </Link>
                    </div>
                </div>
                </div>
                <div className="sort" onClick={() => setDropdown((prev) => !prev)}>
                    <img src="/Sort.svg" alt="sortImg" />
                    <span>Сортировка</span>
                    {
                        dropdown && (
                                <div className="dropdown">
                                <ul className="sort__dropList">
                                    <span className="sort__dropSort">Сортировка:</span>
                                    <li><button type="button">Все</button></li>
                                    <li><button type="button">Популярное</button></li>
                                    <li><button type="button">Новинки</button></li>
                                    <li><button type="button">Горячее</button></li>
                                </ul>
                                </div>
                        )
                    }
                    
                </div>
            </main>
    </div>
  )
}

export default Feed