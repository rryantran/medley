import EditPopup from "./EditPopup";
import DeletePopup from "./DeletePopup";

const Feed = ({ feed, fetchFeeds }) => {
  return (
    <div>
      <div>
        <p>{feed.title}</p>

        <a href={feed.url} target="_blank">
          {feed.url}
        </a>
      </div>

      <div>
        <EditPopup feed={feed} fetchFeeds={fetchFeeds} />
        <DeletePopup feed={feed} fetchFeeds={fetchFeeds} />
      </div>
    </div>
  );
};

export default Feed;
