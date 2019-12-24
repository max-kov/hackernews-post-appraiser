'use strict';
 
const ui = (
    <div class="container">
        <h1>Hackernews post appraiser.</h1>
        <input class="post-title" type="text"/>
        <div id="input-score"/>
    </div>
);

ReactDOM.render(ui, document.getElementById('root'));
