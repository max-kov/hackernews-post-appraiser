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
        <tr>
          <td>{row.title}</td>
          <td>{row.points}</td>
        </tr>
      )
    }); 

    return <table>{tableRows}</table>;
  }
}

export default SimilarPostsTable;
