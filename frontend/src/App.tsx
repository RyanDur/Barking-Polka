import {type FC} from 'react'
import type {AppContextType} from "./AppContext";
import {AppContext} from "./AppContext";
import './App.css'
import {Chat} from "./components/Chat";

const App: FC<AppContextType> = (appContext) => {
  return (
    <AppContext.Provider value={appContext}>
      <h1>HI!</h1>
      <Chat/>
    </AppContext.Provider>
  )
};

export default App
