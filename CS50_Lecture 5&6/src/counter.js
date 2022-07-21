if (!localStorage.getItem('counter')){
    localStorage.setItem('counter', 0);
}


//this initialises a variable that mayyyy be reassigned to something else
// const counter means that it will not be changed anymore
// here must use let because counter will be reassigned.

    function count(){
        let counter = localStorage.getItem('counter');
        counter++;
        document.querySelector('h1').innerHTML = counter;
        localStorage.setItem('counter', counter);
    }

    function reset(){
        localStorage.setItem('counter', 0);
        document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    }

    document.addEventListener('DOMContentLoaded', function(){
        document.querySelector('h1').innerHTML = localStorage.getItem('counter');
        document.querySelector('#counter').addEventListener('click', count);
        document.querySelector('#reset').addEventListener('click', reset);
    });