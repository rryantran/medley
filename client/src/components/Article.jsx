const Article = ({ article }) => {
  const date = new Date(article.pub_date);
  const formattedDate = date.toLocaleString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  });

  return (
    <div>
      <div>
        <a href={article.url} target="_blank">
          {article.title}
        </a>
        <p>By {article.author}</p>
        <p>{formattedDate}</p>
      </div>
      <p>{article.source}</p>
    </div>
  );
};

export default Article;
