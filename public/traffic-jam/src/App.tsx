import React from "react";
import logo from "./logo.svg";
import { BackendContextProvider, MainLayout } from "./shared";
import "./App.css";
import { createTheme } from "@mui/material";
import { ThemeProvider } from "@emotion/react";
import { defaultThemeOptions } from "./themes";
import { Outlet } from "react-router-dom";
import { UserContextProvider } from "./shared/contexts/user-context";

const customTheme = createTheme(defaultThemeOptions);

function App() {
  return (
    <BackendContextProvider>
    <UserContextProvider>
      <ThemeProvider theme={customTheme}>
        <MainLayout>
          <Outlet />
        </MainLayout>
      </ThemeProvider>
    </UserContextProvider>
    </BackendContextProvider>
  );
}

export default App;
