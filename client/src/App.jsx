import axios from "axios";

const App = () => {
  // test route
  axios.get("/api/user/test").then((result) => {
    console.log(result.data.message);
  });

  return <></>;
};

export default App;
