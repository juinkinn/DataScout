import { useState } from "react";

export function useAuth() {
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState(null);

  const loginUser = (t, u) => {
    setToken(t);
    setUsername(u);
  };

  const logoutUser = () => {
    setToken(null);
    setUsername(null);
  };

  return { token, username, loginUser, logoutUser };
}
