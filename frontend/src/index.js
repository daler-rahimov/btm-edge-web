import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

// import AuthLayout from "layouts/Auth.js";
// import RtlLayout from "layouts/RTL.js"; // This is for right to left languages
import AdminLayout from "layouts/Admin.js";

import "assets/scss/material-dashboard-pro-react.scss?v=1.10.0";

ReactDOM.render(
  <BrowserRouter>
    <Switch>
      {/* <Route path="/rtl" component={RtlLayout} />  */}
      {/* <Route path="/auth" component={AuthLayout} /> */}
      <Route path="/admin" component={AdminLayout} />
      <Redirect from="/" to="/admin/dashboard" />
    </Switch>
  </BrowserRouter>,
  document.getElementById("root")
);
