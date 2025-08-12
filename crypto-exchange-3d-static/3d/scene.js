import * as THREE from 'https://esm.sh/three@0.160.0';
import { OrbitControls } from 'https://esm.sh/three@0.160.0/examples/jsm/controls/OrbitControls.js';

export function initScene(root) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(root.clientWidth, root.clientHeight);
  root.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, root.clientWidth / root.clientHeight, 0.1, 200);
  camera.position.set(0, 1.6, 4.2);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enablePan = false;
  controls.minDistance = 2.5;
  controls.maxDistance = 10;

  // Lights
  const hemi = new THREE.HemisphereLight(0x4ac6ff, 0x090d12, 0.6);
  scene.add(hemi);
  const key = new THREE.DirectionalLight(0xffffff, 1.2);
  key.position.set(4, 6, 3);
  scene.add(key);

  // Neon grid floor
  const grid = new THREE.GridHelper(40, 40, 0x23f0c7, 0x112233);
  grid.position.y = -1.2;
  scene.add(grid);

  // Rotating coin
  const coinRadius = 0.9;
  const coinThickness = 0.12;
  const coinGeo = new THREE.CylinderGeometry(coinRadius, coinRadius, coinThickness, 96);
  const gold = new THREE.MeshStandardMaterial({ color: 0xffd166, metalness: 0.9, roughness: 0.2, envMapIntensity: 1.0 });
  const coin = new THREE.Mesh(coinGeo, gold);
  coin.rotation.x = Math.PI * 0.1;
  scene.add(coin);

  // Price ring
  const ringGeo = new THREE.TorusGeometry(coinRadius + 0.25, 0.03, 16, 120);
  const ringMat = new THREE.MeshBasicMaterial({ color: 0x5ad1ff });
  const ring = new THREE.Mesh(ringGeo, ringMat);
  ring.rotation.x = Math.PI * 0.5;
  scene.add(ring);

  const resize = () => {
    const { clientWidth: w, clientHeight: h } = root;
    renderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  window.addEventListener('resize', resize);

  let lastPrice = 0;
  function updatePrice(newPrice) {
    if (!isFinite(newPrice)) return;
    const delta = Math.tanh((newPrice - lastPrice) / Math.max(1, newPrice * 0.001));
    coin.rotation.y += delta * 0.2;
    gold.emissive = new THREE.Color(delta >= 0 ? 0x105a2a : 0x5a1010);
    lastPrice = newPrice;
  }

  let highQuality = true;
  function toggleQuality() {
    highQuality = !highQuality;
    renderer.setPixelRatio(highQuality ? Math.min(devicePixelRatio, 2) : 1);
  }

  const clock = new THREE.Clock();
  function animate() {
    const t = clock.getElapsedTime();
    coin.rotation.y += 0.008;
    ring.material.color.setHSL((t * 0.05) % 1, 0.7, 0.6);
    controls.update();
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  animate();

  return {
    updatePrice,
    toggleQuality,
    getLastPrice: () => lastPrice,
  };
}