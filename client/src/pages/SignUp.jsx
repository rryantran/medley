import axios from "axios";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Alert from "../components/Alert";

const SignUp = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [alert, setAlert] = useState("");
  const [showAlert, setShowAlert] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    const newUser = {
      username: username,
      email: email,
      password: password,
      confirm_password: confirmPassword,
    };

    axios
      .post("/api/auth/signup", newUser)
      .then((res) => {
        console.log(res.data);
        navigate("/login");
      })
      .catch((err) => {
        console.log(err.response.data.message);
        setAlert(err.response.data.message);
        setShowAlert(true);
        setPassword("");
        setConfirmPassword("");
      });
  };

  return (
    <div>
      <h2>Sign Up</h2>

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
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />

        <button onClick={handleSubmit}>Sign Up</button>
      </form>

      <p>
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </div>
  );
};

export default SignUp;
