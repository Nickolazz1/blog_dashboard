/* feature app */
window.onload = init();

var scene, camera, renderer;

function init() {
    var container = document.createElement('div');
    container.className = "app";
    document.body.appendChild(container)
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.y = 150;
    camera.position.z = 600;
    renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    container.appendChild( renderer.domElement );

    // main logic
    scene.add(lines());
    scene.add(mycustom(12));

    // start app
    renderer.render(scene, camera);
}


function lines() {
    var line_geometry = new THREE.Geometry();
    line_geometry.vertices.push(new THREE.Vector3(0,0,0));
    line_geometry.vertices.push(new THREE.Vector3(0,250,0));
    var line = new THREE.Line(line_geometry);
    return line;
}

function mycustom(a) { 
    console.log("Hello custom: ");
    console.log(a)
    var line_geometry = new THREE.Geometry();
    line_geometry.vertices.push(new THREE.Vector3(8,8,8));
    line_geometry.vertices.push(new THREE.Vector3(234,350,0));
    var line = new THREE.Line(line_geometry);
    return line;
}
