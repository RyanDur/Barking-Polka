import {createContext} from "react";

export type AppContextType = {
  env: {
    serverHost?: string
  }
};

export const AppContext = createContext<AppContextType>({env: {serverHost: ''}});