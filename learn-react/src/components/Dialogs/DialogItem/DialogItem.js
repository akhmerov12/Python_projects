import classes from "./../Dialogs.module.css"
import React from 'react';
import {NavLink} from "react-router-dom";

const DialogItem = (props) => {
    return (
        <div className={classes.dialog}>
            <img src={props.url} />
            <NavLink className={classes.name} to={"/dialogs/" + props.id}>{props.name} </NavLink>
        </div>
    )
}

export default DialogItem;