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
      <div className="flex justify-between align-middle px-10 py-6 border-b border-silver">
        <Link
          to="/"
          className="text-4xl underline decoration-8 decoration-pink"
        >
          medley
        </Link>

        <div className="flex gap-8 items-center text-lg">
          <Link
            to="/articles"
            className="hover:underline decoration-2 decoration-pink"
          >
            Articles
          </Link>

          <Link
            to="/feeds"
            className="hover:underline decoration-2 decoration-pink"
          >
            Feeds
          </Link>

          <button
            onClick={handleLogOut}
            className="hover:underline decoration-2 decoration-pink"
          >
            Log Out
          </button>
        </div>
      </div>
    );
  } else {
    return (
      <div className="flex justify-between align-middle px-10 py-6 border-b border-silver">
        <Link
          to="/"
          className="text-4xl underline decoration-8 decoration-pink"
        >
          medley
        </Link>

        <div className="flex gap-8 items-center text-lg">
          <Link
            to="/signup"
            className="hover:underline decoration-2 decoration-pink"
          >
            Sign Up
          </Link>
          <Link
            to="/login"
            className="hover:underline decoration-2 decoration-pink"
          >
            Log In
          </Link>
        </div>
      </div>
    );
  }
};

export default NavBar;
