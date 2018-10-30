window.onload=function () {
    var a=document.getElementsByTagName('a')
    for(i=1;i<a.length;i++){
        a[i].target='_self'
    }
}