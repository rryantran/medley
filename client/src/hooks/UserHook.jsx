import axios from "axios";
import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get("/api/user/current")
      .then((result) => {
        setUser(result.data.user);
        console.log(result.data.user);
      })
      .catch((err) => {
        console.log("No user logged in");
      });
  }, []);

  const login = (user) => {
    return axios.post("/api/auth/login", user).then((res) => {
      console.log(res.data);
      setUser(res.data.id);
      navigate("/");
    });
  };

  const logout = () => {
    return axios.post("/api/auth/logout").then((result) => {
      console.log(result.data.message);
      setUser(null);
      navigate("/");
    });
  };

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  return useContext(UserContext);
};
