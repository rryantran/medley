import { Link } from "react-router-dom";
import "../index.css";

const Home = () => {
  return (
    <div>
      <h1 className="text-7xl">Find your perfect blend.</h1>

      <p>Aggregate content from all your favorite feeds, all in one place.</p>

      <div>
        <Link to="/signup">Sign Up</Link>
        <Link to="/login">Log In</Link>
      </div>
    </div>
  );
};

export default Home;
