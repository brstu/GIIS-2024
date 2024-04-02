import {
  CANVAS_ID,
  MAP_SIZE,
  SCORE_ID,
  SNAKE_END_SPEED,
  SNAKE_RECT_BORDER_COLOR,
  SNAKE_RECT_BORDER_WIDTH,
  SNAKE_RECT_FILL_COLOR,
  SNAKE_START_SPEED,
  SNAKE_START_SPEED_ADDITION,
  cellSize,
} from "../settings";
import { drawRect } from "./draw-lib/draw-rect";

class Snake {
  constructor() {
    this.create();
  }

  create() {
    this.body = [
      { x: Math.round(MAP_SIZE / 2 + 0.5), y: Math.round(MAP_SIZE / 2 + 0.5) },
    ];
    this.direction = { x: 0, y: -1 };
    this.speed = SNAKE_START_SPEED;
    this.lastStepTime = 0;
  }

  isCrashed() {
    const head = this.body[0];
    for (let i = 1; i < this.body.length; i++) {
      if (this.body[i].x === head.x && this.body[i].y === head.y) {
        this.create();
        const scoreItem = document.getElementById(SCORE_ID);
        scoreItem.textContent = 0;
      }
    }
  }

  getLen() {
    return this.body.length - 1;
  }

  move() {
    if (Date.now() - this.lastStepTime > this.speed) {
      const newHeadPos = {
        x: (this.body[0].x + this.direction.x + MAP_SIZE) % MAP_SIZE,
        y: (this.body[0].y + this.direction.y + MAP_SIZE) % MAP_SIZE,
      };
      this.body.unshift(newHeadPos);
      this.body.pop();
      this.lastStepTime = Date.now();
    }
  }

  addSpeed() {
    this.speed = Math.max(
      SNAKE_END_SPEED,
      this.speed - SNAKE_START_SPEED_ADDITION
    );
  }

  addLength() {
    const newNode = this.body[this.body.length - 1];
    const newHeadPos = {
      x: (this.body[0].x + this.direction.x + MAP_SIZE) % MAP_SIZE,
      y: (this.body[0].y + this.direction.y + MAP_SIZE) % MAP_SIZE,
    };
    this.body.unshift(newHeadPos);
    this.body.pop();
    this.body.push(newNode);
  }

  getHeadPos() {
    return this.body[0];
  }

  setDirection(newDirection) {
    if (
      Math.abs(newDirection.x - this.direction.x) % 2 === 0 ||
      Math.abs(newDirection.y - this.direction.y) % 2 === 0
    )
      return;
    this.direction = newDirection;
  }

  draw() {
    const canvas = document.getElementById(CANVAS_ID);
    const context = canvas.getContext("2d");
    for (let rect of this.body) {
      drawRect(
        context,
        SNAKE_RECT_BORDER_WIDTH,
        SNAKE_RECT_BORDER_COLOR,
        SNAKE_RECT_FILL_COLOR,
        rect.x * cellSize,
        rect.y * cellSize,
        (rect.x + 1) * cellSize,
        (rect.y + 1) * cellSize
      );
    }
  }
}

export const snake = new Snake();
