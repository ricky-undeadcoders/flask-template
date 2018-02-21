var canvas = document.createElement('canvas');
var ctx = canvas.getContext('2d');
canvas.id = 'img_canvas';
canvas.width = 208;
canvas.height = 208;
document.body.appendChild(canvas);

$('#img_canvas').appendTo('#homepage_img_div');

var skeleton = {
    x : 104,
    y : 104,
    image : new Image()
};
var left_eye = {
    x : 138,
    y : 100,
    radius : 8
};
var right_eye = {
    x : 72,
    y : 100,
    radius : 8
};
var mouse = {
    x : null,
    y : null,
    changed : false,
    changeCount : 0
};

skeleton.image.src = skeleton_src;

function drawSkeleton(img, x, y, lookx, looky){
    ctx.setTransform(1, 0, 0, 1, x, y);
    ctx.drawImage(img, -img.width / 4, -img.height / 4, 256, 256);
    ctx.setTransform(1, 0, 0, 1, 0, 0); // restore default not needed if you use setTransform for other rendering operations
}

function drawEye(x,y,radius,color, lookx, looky){
    ctx.strokeStyle = 'black';
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.setTransform(1, 0, 0, 1, x, y);
    ctx.rotate(Math.atan2(looky - y, lookx - x));
    ctx.translate(6, 0);
    ctx.arc(0, 0, radius, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.fill();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
}

function mouseEvent(e) {  // get the mouse coordinates relative to the canvas top left
    var bounds = canvas.getBoundingClientRect();
    mouse.x = e.pageX - bounds.left;
    mouse.y = e.pageY - bounds.top;
    mouse.cx = e.clientX - bounds.left; // to compare the difference between client and page coordinates
    mouse.cy = e.clientY - bounds.top;
    mouse.changed = true;
    mouse.changeCount += 1;
}
document.addEventListener("mousemove",mouseEvent);
// only render when the DOM is ready to display the mouse position
function update(){
    if(skeleton.image.complete || mouse.changed){ // only render when image ready and mouse moved
        mouse.changed = false; // flag that the mouse coords have been rendered
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // get mouse canvas coordinate correcting for page scroll
        var x = mouse.x - scrollX;
        var y = mouse.y - scrollY;
        drawSkeleton(skeleton.image, skeleton.x, skeleton.y, x ,y);
        drawEye(left_eye.x, left_eye.y, left_eye.radius, "white", x, y);
        drawEye(right_eye.x, right_eye.y, right_eye.radius, "white", x, y);
    }
    requestAnimationFrame(update);
}
requestAnimationFrame(update);