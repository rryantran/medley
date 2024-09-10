import Alert from "../components/Alert";
import { useState } from "react";
import { Link } from "react-router-dom";
import { useUser } from "../hooks/UserHook";

const SignUp = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [alert, setAlert] = useState("");
  const [showAlert, setShowAlert] = useState(false);

  const { login } = useUser();

  const handleLogIn = (e) => {
    e.preventDefault();

    const user = { username, password };

    login(user).catch((err) => {
      console.log(err.response.data.message);
      setAlert(err.response.data.message);
      setShowAlert(true);
      setPassword("");
    });
  };

  return (
    <div>
      <h2>Log In</h2>

      {showAlert && (
        <Alert
          message={alert}
          clickHanlder={() => {
            setShowAlert(false);
          }}
        />
      )}

      <form>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleLogIn}>Log In</button>
      </form>

      <p>
        Don't have an account? <Link to="/signup">Create one</Link>
      </p>
    </div>
  );
};

export default SignUp;
