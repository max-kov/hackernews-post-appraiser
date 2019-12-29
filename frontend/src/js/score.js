'use strict';

class Score extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <h4>I think your post will receive {this.props.score} points</h4>
      </div>
    );
  }
}

export default Score;
