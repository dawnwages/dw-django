let navState = 'close';


function closeNav(e) {
    if (navState == 'open') {
        document.getElementById("mySidenav").style.width = "0vw";
        document.getElementById("l1").style.transform = null;
        document.getElementById("l2").style.transform = null;
        document.getElementById("l3").style.display = 'inherit';
        navState = 'close';
    } else {
        document.getElementById("mySidenav").style.width = "100vw";
        document.getElementById("l1").style.transform = 'matrix(1.1, -1, 0, 1, -1, 10)';
        document.getElementById("l2").style.transform = 'matrix(1.79, 1, 0, 1, 0, -10)';
        document.getElementById("l3").style.display = 'none';
        navState = 'open';
    }

}