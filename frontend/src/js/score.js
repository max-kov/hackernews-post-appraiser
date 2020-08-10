'use strict';

class Score extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <h4>I think your post will receive <div class="score-value">{this.props.score}</div> points</h4>
      </div>
    );
  }
}

export default Score;
