let navState = 'open';

function openNav() {

}

function closeNav() {
    if (navState == 'open') {
        document.getElementById("mySidenav").style.width = "0vw";
        document.getElementById("opaqueContainer").style.backgroundColor = "transparent";
        console.log('close');
        navState = 'close';
    } else {
        document.getElementById("mySidenav").style.width = "inherit";
        document.getElementById("opaqueContainer").style.backgroundColor = null;
        console.log('open');
        navState = 'open';
    }

}