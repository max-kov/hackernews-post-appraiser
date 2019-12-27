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

  handleChange = event => {
    const self = this;

    self.setState({
      inputValue: event.target.value,
    });

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/score-post');
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    xhr.onreadystatechange = () => {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        self.setState({
          score: xhr.responseText,
          wasFetched: true,
        });
      }
    }

    xhr.send(JSON.stringify(event.target.value));
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
