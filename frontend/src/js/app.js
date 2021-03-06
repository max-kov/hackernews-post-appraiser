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
  };

  render() {
    const white = {backgroundColor: "rgb(255, 255, 255)"}
    const red = {backgroundColor: "rgb(241, 144, 131)"}
    const blue = {backgroundColor: "rgb(157, 212, 254)"}
    const green = {backgroundColor: "rgb(174, 252, 191)"}

    var style = white;
    if (!this.state.wasFetched) {
      style = white;
    } else if (this.state.score > 50){
      style = green;
    } else if (this.state.score > 10){
      style = blue;
    } else {
      style = red;
    }

    return (
      <div className="container">
        <div className="test-input" style={style} onChange={this.handleChange}>
          <h1>Hackernews post appraiser</h1>
          <TitleTextArea/>
          <Score score={this.state.score}/>
        </div>
      </div>
    )
  }
}

ReactDOM.render(<App />, document.getElementById('root'));
