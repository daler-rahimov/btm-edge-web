import React, { useEffect } from "react";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import LoginPage from "./views/UserProfile/LoginPage";
import { Provider } from "react-redux";
import store from "./store";
import AuthProvider from "./utils/authProvider";
import oauth, { loadUserFromStorage } from "./services/oauth";
import PrivateRoute from "./utils/protectedRoute";

// core components
import AuthLayout from "layouts/Auth.js";
// import RtlLayout from "layouts/RTL.js"; // This is for right to left languages
import AdminLayout from "layouts/Admin.js";

function App() {
  useEffect(() => {
    // fetch current user
    loadUserFromStorage(store);
  }, []);

  return (
    <Provider store={store}>
      <AuthProvider userManager={oauth} store={store}>
        <BrowserRouter>
          <Switch>
            <PrivateRoute path="/admin/user" component={AdminLayout} />
            <PrivateRoute path="/admin" component={AdminLayout} />

            <Route path="/login-page" component={LoginPage} />
            <Route path="/auth" component={AuthLayout} />

            <Redirect from="/" to="/admin/dashboard" />
          </Switch>
        </BrowserRouter>
      </AuthProvider>
    </Provider>
  );
}

export default App;
