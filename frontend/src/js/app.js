'use strict';

import Score from "./score.js"
import TitleTextArea from "./title-text-area.js"
import SimilarPostsTable from "./similar-posts-table.js"
 
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inputValue: "",
      score: '0',
      wasFetched: false,
      similarPosts: [],
    };
  }

  // arrow function is important here, so that we dont redifine 'this'
  handleChange = event => {
    // TODO: put a rate limit on the requests
    const self = this;

    const newTitle = event.target.value;

    self.setState({
      inputValue: newTitle,
    });

    var scoreXhr = new XMLHttpRequest();
    scoreXhr.open('POST', '/api/score-post');
    scoreXhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    scoreXhr.onreadystatechange = () => {
      if (scoreXhr.readyState === XMLHttpRequest.DONE && scoreXhr.status === 200) {
        self.setState({
          score: scoreXhr.responseText,
          wasFetched: true,
        });
      }
    }

    scoreXhr.send(JSON.stringify(newTitle));

    var similarPostsXhr = new XMLHttpRequest();
    similarPostsXhr.open('GET', `https://hn.algolia.com/api/v1/search?query=${newTitle}&tags=story`);

    similarPostsXhr.onreadystatechange = () => {
      if (similarPostsXhr.readyState === XMLHttpRequest.DONE && similarPostsXhr.status === 200) {
        self.setState({
          similarPosts: JSON.parse(similarPostsXhr.responseText),
        });
      }
    }

    similarPostsXhr.send();
  };

  render() {
    return (
      <div className="container">
        <div className="test-input" onChange={this.handleChange}>
          <h1>Hackernews post appraiser</h1>
          <TitleTextArea/>
          <Score score={this.state.score}/>
        </div>
        <h2>Post statistics</h2>
        <p>bla bla bla</p>
      </div>
    )
  }
}

ReactDOM.render(<App />, document.getElementById('root'));
