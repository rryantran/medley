const Alert = ({ message, clickHanlder }) => {
  return (
    <div>
      <div>{message}</div>
      <button onClick={clickHanlder}>&times;</button>
    </div>
  );
};

export default Alert;
