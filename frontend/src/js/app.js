'use strict';

import Score from "./score.js"
import TitleTextArea from "./title-text-area.js"
 
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inputValue: ""
    };
  }

  handleChange = event => {
    this.setState({
      inputValue: event.target.value
    });
  };

  render() {
    return (
      <div className="container" onChange={this.handleChange}>
        <h1>Hackernews post appraiser.</h1>
        <TitleTextArea/>
        <Score titleText={this.state.inputValue}/>
      </div>
    )
  }
}

ReactDOM.render(<App />, document.getElementById('root'));
