'use strict';

class Score extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <h4>I think your post will receive</h4>
        <div className="score-value">{this.props.score}</div>
        <h4>points</h4>
      </div>
    );
  }
}

export default Score;
