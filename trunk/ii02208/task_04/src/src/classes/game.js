import { SCORE_ID } from "../settings";
import { bonus } from "./bonus";
import { map } from "./game-map";
import { snake } from "./snake";

class Game {
  constructor() {
    this.map = map;
    this.snake = snake;
    this.bonus = bonus;
  }

  keyPressEvent(event) {
    switch (event.key) {
      case "ArrowUp":
        this.snake.setDirection({ x: 0, y: -1 });
        break;
      case "ArrowDown":
        this.snake.setDirection({ x: 0, y: 1 });
        break;
      case "ArrowLeft":
        this.snake.setDirection({ x: -1, y: 0 });
        break;
      case "ArrowRight":
        this.snake.setDirection({ x: 1, y: 0 });
        break;
      default:
    }
  }

  isSnakeSelectBonus() {
    const headPos = this.snake.getHeadPos();
    if (bonus.isSelected(headPos.x, headPos.y)) {
      this.score++;
      this.snake.addLength();
      const scoreItem = document.getElementById(SCORE_ID);
      scoreItem.textContent = this.snake.getLen();
      this.snake.addSpeed();
      bonus.create();
    }
  }

  eventLoop() {
    this.map.draw();
    this.bonus.draw();
    this.snake.draw();
    this.snake.move();
    this.snake.isCrashed();
    this.isSnakeSelectBonus();
  }
}

export const game = new Game();
document.addEventListener("keydown", game.keyPressEvent.bind(game));
