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

    return tableEntries.map((row) => {
      return (
        <tr>
          <td>{row.title}</td>
          <td>{row.points}</td>
        </tr>
      )
    }); 
  }
}

export default SimilarPostsTable;
