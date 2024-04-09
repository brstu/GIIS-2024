import {
  CANVAS_ID,
  MAP_SIZE,
  BONUS_BORDER_COLOR,
  BONUS_BORDER_WIDTH,
  BONUS_FILL_COLOR,
  cellSize,
} from "../settings";
import { drawRect } from "./draw-lib/draw-rect";

class Bonus {
  constructor() {
    this.create();
  }

  isSelected(x, y) {
    return x === this.pos.x && y === this.pos.y;
  }

  create() {
    const x = Math.round(Math.random() * (MAP_SIZE - 1));
    const y = Math.round(Math.random() * (MAP_SIZE - 1));
    this.pos = { x, y };
  }

  draw() {
    const canvas = document.getElementById(CANVAS_ID);
    const context = canvas.getContext("2d");
    drawRect(
      context,
      BONUS_BORDER_WIDTH,
      BONUS_BORDER_COLOR,
      BONUS_FILL_COLOR,
      this.pos.x * cellSize,
      this.pos.y * cellSize,
      (this.pos.x + 1) * cellSize,
      (this.pos.y + 1) * cellSize
    );
  }
}

export const bonus = new Bonus();
