import React from "react";
import { Route, Redirect } from "react-router-dom";
import { useSelector } from "react-redux";
import PropTypes from "prop-types";

function ProtectedRoute({ component, ...rest }) {
  const user = useSelector((state) => state.auth.user);

  return user ? (
    <Route {...rest} component={component} />
  ) : (
    <Redirect to={"/auth/login-page"} />
  );
}

ProtectedRoute.propTypes = {
  component: PropTypes.func,
};

export default ProtectedRoute;
