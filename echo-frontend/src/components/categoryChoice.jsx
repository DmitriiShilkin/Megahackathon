import { useState } from 'react';
import { Link } from 'react-router-dom';

const Choice = () => {

    const [active, setActive] = useState()
    const toggleColor = (index) => {
        setActive(index)
    }

    return (
        <div>
            <div className="create__header">
                <button type="button" className='create__backBtn'>
                    <img src="/back.svg" alt="arrow" className='create__arrBack' />
                </button>
                <span className='create__title'>Выбор категории</span>
            </div>
            <div className="choice__categories">
                <div className="create__background">
                    <img src="/Spiral 4.png" alt="" className='spiral3'/>
                    <img src="/Spiral 3.png" alt="" className='spiral4'/>
                </div>
                <div className="choice__mainContainer">
                    <div className="choice__firstContainer">
                        <button type="button" className= {active === 0 ? 'category__books active' : 'category__books'} onClick={() => toggleColor(0)}><span className='category__span'>Книги</span></button>
                        <button type="button" className={active === 1 ? 'category__exibitions active' : 'category__exibitions'} onClick={() => toggleColor(1)}><span className='category__span'>Выставки</span></button>
                    </div>
                    <div className="choice__secondContainer">
                        <button type="button" className={active === 2 ? 'category__shows active' : 'category__shows'} onClick={() => toggleColor(2)}><span className='category__span'> Кино и сериалы</span></button>
                        <button type="button" className={active === 3 ? 'category__food active' : 'category__food'} onClick={() => toggleColor(3)}><span className='category__span'>Кафе и рестораны</span></button>
                    </div>
                    <div className="choice__thirdContainer">
                    <button type="button" className={active === 4 ? 'category__concerts active' : 'category__concerts'} onClick={() => toggleColor(4)}><span className='category__span'>Концерты и спектакли</span></button>
                    </div>
                    <div className="create__buttons"> 
                        <button type="button" className='create__choiceBtn'>Выбрать</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Choice