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
          <td class="post-title">{row.title}</td>
          <td class="post-score">{row.points}</td>
        </tr>
      )
    }); 

    return <table><tbody>{tableRows}</tbody></table>;
  }
}

export default SimilarPostsTable;
