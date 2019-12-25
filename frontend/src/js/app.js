'use strict';

 
class App extends React.Component {
    render() {
        return (
            <div className="container">
                <h1>Hackernews post appraiser.</h1>
                <input className="post-title" type="text"/>
            </div>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('root'));
