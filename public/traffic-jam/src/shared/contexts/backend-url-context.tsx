import axios from "axios";
import jwtDecode from "jwt-decode";
import { createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { environment } from "../../environments/environment";

const BackendContext = createContext<BackendContextValue | any>({});

interface Props {
  children: JSX.Element
}

interface BackendContextValue {
  url: string;
  changeUrl: (selectedValue: string) => void;
}

const BackendContextProvider = ({ children }: Props) => {
  const [url, setUrl] = useState(environment.openfaas_url);

  const changeUrl = (selectedValue: string) => {
    switch (selectedValue) {
        case 'OpenFaaS':
            setUrl(environment.openfaas_url);
            break;
        case 'Apache OpenWhisk':
            setUrl(environment.apache_openwhisk_url);
            break;
        case 'Fission':
            setUrl(environment.fission_url);
            break;
        default:
            setUrl(environment.openfaas_url);
      }
  }

  const value = {
    url,
    changeUrl
  }

  return (
    <BackendContext.Provider value={value}>
      {children}
    </BackendContext.Provider>
  )
}

export { BackendContextProvider, BackendContext };
export type { BackendContextValue };