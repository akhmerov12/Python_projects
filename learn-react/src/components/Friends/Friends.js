import React from "react";
import classes from './Friends.module.css'
import DialogItem from "../Dialogs/DialogItem/DialogItem";

let Friends = (props) => {

    let friendElements = props.state.map(dialog => <DialogItem name={dialog.name} id={dialog.id} url = {dialog.url}/>)
    return (
        <div className={classes.friendsPage}>
            <div>
                My Friends ({props.state[props.state.length - 1].id})
            </div>

            <div>
                {friendElements}
            </div>
        </div>
    )
}

export default Friends;