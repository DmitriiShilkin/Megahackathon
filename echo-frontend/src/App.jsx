import React, { useEffect } from "react";
import { useState } from "react";
import axios from "axios";
import Feed from "./components/feed";
import PostPage from "./components/post";
import Fyp from "./components/fyp";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SharedLayouts from "./components/sharedLayouts";
import CreatiingPost from "./components/creatingPost"
import CategoryChoice from "./components/categoryChoice"
import Error from "./components/error";
import "./css/index.css";

const App = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/v1/posts/");
        const responseData = response.data.results;
        setPosts(responseData);
      } catch (error) {
        console.error(error);
      }
    };
    fetchPosts();
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" index element={<SharedLayouts />} />
        <Route
          path="/feed"
          element={
            posts.map((item) => (
            <PostPage key={item.id} item={item} />
          ))}
        />
        <Route path="/feed" element={<Feed />} />
        <Route path="/feed/fyp" element={<Fyp />} />
        <Route path = "/creatingPost" element = {<CreatiingPost />} />
        <Route path = "/creatingPost/choice" element = {< CategoryChoice/>} />
        <Route path="*" element={<Error />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;