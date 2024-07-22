function popUp(message, category = 'info') {
    ul = document.getElementById('popUp');

    tmpItem = document.createElement('li');
    tmpItem.className = category;
    tmpItem.innerHTML = message;
    const id = Math.random().toString(36).substr(2, 9);
    tmpItem.id = id;


    ul.appendChild(tmpItem);

    setTimeout(() => {
        document.getElementById(id).remove();
    }, 5000);
}
