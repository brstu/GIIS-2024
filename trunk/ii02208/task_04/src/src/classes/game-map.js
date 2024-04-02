import {
  CANVAS_ID,
  MAP_SIZE,
  MAP_BG_COLOR,
  MAP_LINE_WIDTH,
  MAP_LINE_COLOR,
  CANVAS_SIZE,
} from "../settings";
import { drawLine } from "./draw-lib/draw-line";

class GameMap {
  constructor() {
    this.map = [];
    for (let i = 0; i < MAP_SIZE; i++) {
      const row = [];
      for (let j = 0; j < MAP_SIZE; j++) {
        row.push(0);
      }
      this.map.push(row);
    }
    console.log(this.map);
  }

  draw() {
    const canvas = document.getElementById(CANVAS_ID);
    const context = canvas.getContext("2d");
    context.fillStyle = MAP_BG_COLOR;
    context.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    const step = CANVAS_SIZE / MAP_SIZE;
    for (let i = step; i < CANVAS_SIZE; i += step) {
      drawLine(context, MAP_LINE_WIDTH, MAP_LINE_COLOR, i, 0, i, CANVAS_SIZE);
      drawLine(context, MAP_LINE_WIDTH, MAP_LINE_COLOR, 0, i, CANVAS_SIZE, i);
    }
  }
}

export const map = new GameMap();
