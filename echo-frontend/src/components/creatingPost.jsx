import { Link } from 'react-router-dom';
import * as React from 'react';
import Box from '@mui/material/Box';
import Rating from '@mui/material/Rating';
import Typography from '@mui/material/Typography';

const CreatingPost = () => {

    //рейтинг
    const [value, setValue] = React.useState(0);

    return (
        <div>
            <div className="create__header">
                <button type="button" className='create__backBtn'>
                    <img src="/back.svg" alt="arrow" className='create__arrBack' />
                </button>
                <span className='create__title'>Создание поста</span>
            </div>
            <div className="create__categories">
                <span className="create__chooseCategory">Выбор категории</span>
                <Link to='choice'>
                    <button type="button" className='create__categoryBtn'>
                        <span className="create__categoryList">
                            Список категорий
                        </span>
                        <img src="/forward.svg" alt="" className='create__forwardBtn' />
                    </button>
                </Link>
            </div>
            <div className="create__postContainer">
                <div className="create__postTitle">
                    <span className="create__titleSpan">Заголовок</span>
                    <textarea name="createTitle" className='create__titleTextarea' placeholder='Заголовок...' method = 'post'></textarea>
                </div>
                <div className="create__textBody">
                    <span className="create__bodySpan">Текст поста</span>
                    <textarea name="createTitle" className='create__bodyTextarea' placeholder='Текст поста...' method = 'post'></textarea>
                </div>
                <div className="create__raiting">
                    <span className="create__raitingName">Оценка</span>
                <Box
      sx={{
        '& > legend': { mt: 2 },
      }}
    >
      <Typography component="legend"></Typography>
      <Rating
        name="simple-controlled"
        value={value}
        onChange={(event, newValue) => {
          setValue(newValue);
        }}
      />
    </Box>
                </div>
                <div className="create__postPhotos">
                    <img src="/choosePhoto.svg" alt="photoIcon" />
                </div>
                <div className="create__buttons">
                    <button type="submit" className='create__sendBtn disabled'>Отправить</button>
                    <button type="button" className='create__saveBtn'>Сохранить</button>
                </div>
            </div>
        </div>
    )
} 

export default CreatingPost