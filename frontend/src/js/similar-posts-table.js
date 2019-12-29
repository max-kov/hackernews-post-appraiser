'use strict';

class SimilarPostsTable extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const tableEntries = this.props.posts.hits;

    if (typeof tableEntries === 'undefined' || tableEntries === null) {
      return null;
    }

    const tableRows = tableEntries.map((row) => {
      return (
        <tr key={row.objectID}>
          <td class="post-title" align="left">{row.title}</td>
          <td class="post-score" align="right">{row.points}</td>
        </tr>
      )
    }); 

    return (
      <div>
        <span>Similar posts:</span>
        <table><tbody>{tableRows}</tbody></table>;
      </div>
    )
  }
}

export default SimilarPostsTable;
