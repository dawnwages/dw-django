let navState = 'close';


function closeNav(e) {
    if (navState == 'open') {
        document.getElementById("mySidenav").style.width = "0vw";
        document.getElementById("l1").style.transform = null;
        document.getElementById("l2").style.transform = null;
        document.getElementById("l3").style.display = 'inherit';
        document.getElementById("side-nav").style.right = '10rem';
        navState = 'close';

    } else {
        document.getElementById("mySidenav").style.width = "24rem";
        document.getElementById("l1").style.transform = 'matrix(1, -1, 0, 1.1, 0, 9)';
        document.getElementById("l2").style.transform = 'matrix(1, 1, 0, 1, .5, -17)';
        document.getElementById("l3").style.display = 'none';
        document.getElementById("side-nav").style.right = '26rem';
        navState = 'open';
    }
 console.log(navState);
}