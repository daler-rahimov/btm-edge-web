import React from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import styles from "assets/jss/material-dashboard-pro-react/views/dashboardStyle.js";

const useStyles = makeStyles(styles);

export default function WirelessConnection() {
  const classes = useStyles();
  return (
    <div>
      <h4 className={classes.cardIconTitle}>
        Wireless Connection page goes here
      </h4>
    </div>
  );
}
