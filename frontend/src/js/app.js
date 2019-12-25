'use strict';
 
class App extends React.Component {
    render() {
        return (
            <div class="container">
                <h1>Hackernews post appraiser.</h1>
                <input class="post-title" type="text"/>
                <div id="input-score"/>
            </div>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('root'));
