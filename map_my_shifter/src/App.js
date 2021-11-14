import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { Provider } from "react-redux";
import { Content } from "@carbon/ibm-security";
import "./App.scss";
import Header from "./components/Header";
import Welcome from "./components/Welcome/Welcome";
import About from "./components/About";
import store from "./store/store";
import FrameFromSTIX from "./components/FromSTIX/FrameFromSTIX";
import FrameToSTIX from "./components/ToSTIX/FrameToSTIX";

function App() {
  return (
    <Provider store={store}>
      <Router>
        <Header />
        <Content>
          <Switch>
            <Route path="/from_stix">
              <FrameFromSTIX />
            </Route>
            <Route path="/to_stix">
              <FrameToSTIX />
            </Route>
            <Route path="/about">
              <About />
            </Route>
            <Route path="/">
              <Welcome />
            </Route>
          </Switch>
        </Content>
      </Router>
    </Provider>
  );
}

export default React.memo(App);
