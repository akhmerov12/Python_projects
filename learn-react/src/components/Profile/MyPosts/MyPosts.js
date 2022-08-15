import React from 'react'
import Post from "./Post/Post";
import classes from "./MyPosts.module.css";


const MyPosts = (props) => {


    let postsElements = props.posts.map(post => <Post message={post.message} count={post.likesCount}/>)

    return (
        <div className={classes.postsBlock}>
            My post
            <div>
                <div>
                    <textarea></textarea>
                </div>
                <div>
                    <button>Add post</button>
                </div>
            </div>
            <div className={classes.posts}>
                {postsElements}
            </div>
        </div>
    );
}


export default MyPosts;