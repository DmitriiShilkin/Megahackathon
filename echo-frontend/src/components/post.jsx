import { Avatar } from "@mui/material"
import { useState } from "react";
import * as React from 'react';
import Box from '@mui/material/Box';
import Rating from '@mui/material/Rating';
import Typography from '@mui/material/Typography';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Link } from "react-router-dom";


const PostPage = (props) => {
    const current = new Date();
    const date = `${current.getDate()}.${current.getMonth()+1}.${current.getFullYear()}`
    
    const [postDropDown, setPostDropDown] = useState(false)

    //рейтинг
    const [value, setValue] = React.useState(0);
    
    return (
        <div className="post">
            <div className="post__wrapper">
            <Avatar className="post__avatar">Н</Avatar>
            <span className="userName"></span>
            <div className="post__dropDown">
                <div className="post__dotContainer" onClick={()=> setPostDropDown((prev) => !prev)}>
                <div className="post__dot"></div>
                <div className="post__dot"></div>
                <div className="post__dot"></div>
                </div>
            <span className="date"></span>
            </div>
            {
                        postDropDown && (
                            <div className="post__dropdownBody" >
                            <div className="post__dropdownDiv">
                            <ul className="post__dropList">
                                <li>
                                    <img src="/subscribeIcon.svg" alt="subscribe" />
                                    <button type="button">Подписаться</button>
                                </li>
                                <li>
                                     <img src="/bookmark.svg" alt="subscribe" />
                                    <button type="button">Добавить в избранное</button>
                                </li>
                                <li>
                                     <img src="/copyLink.svg" alt="subscribe" />
                                    <button type="button">Скопировать ссылку</button>
                                </li>
                                <li>
                                     <img src="/reportIcon.svg" alt="subscribe" />
                                    <button type="button">Пожаловаться на публикацию</button>
                                </li>
                                <li>
                                    <img src="/NotInteresting.svg" alt="subscribe" />   
                                    <button type="button">Это неинтересно</button>
                                </li>
                            </ul>
                            </div>
                            </div>
                        )
                    }
                     </div>
            <div className="post__body">
                <h2 className="title">{props.item.headline}</h2>
                <div className="rating">
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
                <div className="post__images">
                <div className="post__sliderDots">
                </div>
                </div>
                <p className="description">{props.item.text}</p>
                <div className="post__likesComments">
                    <div className="post__likes"></div>
                    <img src="/likeIcon.svg" alt="like" />
                    <span className="post__likesNum"></span>
                    <div className="post__comments">
                    <img src="/commentIcon.svg" alt="" />
                    <span className="post__commentsNum"></span>
                    </div>
                </div> 
            </div>
        </div>
        

    )
}

export default PostPage