'use strict';

import Score from "./score.js"
import TitleTextArea from "./title-text-area.js"
 
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inputValue: "",
      score: '0',
      wasFetched: false,
    };
  }

  // arrow function is important here, so that we dont redifine 'this'
  handleChange = event => {
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
    return (
      <div className="container" onChange={this.handleChange}>
        <h1>Hackernews post appraiser.</h1>
        <TitleTextArea/>
        {this.state.wasFetched && <Score score={this.state.score}/>}
      </div>
    )
  }
}

ReactDOM.render(<App />, document.getElementById('root'));
