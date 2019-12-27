'use strict';

class Score extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return <span>{this.props.score}</span>;
  }
}

export default Score;
