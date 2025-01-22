const applyButtons = document.querySelectorAll(".card-buttons .apply-btn");
const image = document.getElementById("hand-img");
const bounds = image.getBoundingClientRect();

let posX = 0,
  posY = 0;
let entered = false;
let isPressed = false;

const defImgX = window.innerWidth - bounds.width;
const defImgY = -bounds.height;

let imgX = defImgX;
let imgY = defImgY;
const speed = 0.05;

document.addEventListener("mousemove", (e) => {
  posX = e.clientX;
  posY = e.clientY;
});

applyButtons.forEach((button) => {
  button.addEventListener("mouseover", (e) => {
    if (!button.contains(e.relatedTarget)) {
      image.style.visibility = "visible";
      entered = true;
      animate();
    }
  });

  button.addEventListener("mousedown", () => {
    if (isPressed) return;
    isPressed = true;
    image.style.transform = "translate(-50%, calc(-50% + 10px))";
  });

  button.addEventListener("mouseup", () => {
    if (!isPressed) return;
    isPressed = false;
    image.style.transform = "translate(-50%, -50%)";
  });

  button.addEventListener("mouseleave", () => {
    entered = false;
    setTimeout(() => {
      if (!entered) {
        image.style.visibility = "hidden";
      }
    }, 500);
  });
});

function animate() {
  if (!entered) {
    // Возвращаем изображение в центр
    imgX += (defImgX - imgX) * speed;
    imgY += (defImgY - imgY) * speed;

    // Если картинка уже в центре, останавливаем анимацию
    if (Math.abs(imgX - defImgX) < 0.5 && Math.abs(imgY - defImgY) < 0.5) {
      imgX = defImgX;
      imgY = defImgY;
      return;
    }
  } else {
    // Движение изображения к курсору
    imgX += (posX - imgX - 5) * speed;
    imgY += (posY - bounds.height / 2 - imgY - 10) * speed;
  }

  // Обновляем позицию изображения
  image.style.left = `${imgX}px`;
  image.style.top = `${imgY}px`;

  // Запрашиваем следующий кадр анимации
  requestAnimationFrame(animate);
}
