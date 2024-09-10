import { Link } from "react-router-dom";
import { useUser } from "../hooks/UserHook";

const NavBar = () => {
  const { user, logout } = useUser();

  const handleLogOut = (e) => {
    e.preventDefault();

    logout().catch((err) => {
      console.log(err);
    });
  };

  if (user) {
    return (
      <div>
        <Link to="/">medley</Link>

        <div>
          <Link to="/articles">Articles</Link>
          <Link to="/feeds">Feeds</Link>
          <button onClick={handleLogOut}>Log Out</button>
        </div>
      </div>
    );
  } else {
    return (
      <div className="flex justify-between px-10 py-4">
        <Link to="/" className="text-4xl">
          medley
        </Link>

        <div className="flex">
          <Link to="/signup">Sign Up</Link>
          <Link to="/login">Log In</Link>
        </div>
      </div>
    );
  }
};

export default NavBar;
