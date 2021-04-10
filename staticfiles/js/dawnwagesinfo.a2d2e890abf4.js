let navState = 'close';
let mobile = false;
let sideNavWidth = 24;
let smallScreenWidth = 15;
let xSmallScreenWidth = 10;

function closeNav(e) {
    if (screen.width < 482) {
        sideNavWidth = smallScreenWidth;
    }

    if (screen.width < 322){
        sideNavWidth = xSmallScreenWidth;
    }

    if (navState == 'open') {
        document.getElementById("mySidenav").style.width = "0vw";
        document.getElementById("l1").style.transform = null;
        document.getElementById("l2").style.transform = null;
        document.getElementById("l3").style.display = 'inherit';
        document.getElementById("side-nav").style.right = "5rem";
        navState = 'close';

    } else {
        document.getElementById("mySidenav").style.width = sideNavWidth + "rem";
        document.getElementById("l1").style.transform = 'matrix(1, -1, 0, 1.1, 0, 9)';
        document.getElementById("l2").style.transform = 'matrix(1, 1, 0, 1, .5, -17)';
        document.getElementById("l3").style.display = 'none';
        document.getElementById("side-nav").style.right = sideNavWidth + 2 + "rem";
        navState = 'open';
    }
 console.log(navState, screen.width, sideNavWidth);
}