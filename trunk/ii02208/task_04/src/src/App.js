import { useEffect } from "react";
import { game } from "./classes/game";
import { FRAME_RATE, CANVAS_ID, CANVAS_SIZE, SCORE_ID } from "./settings";

const App = () => {
  useEffect(() => {
    setInterval(() => game.eventLoop(), 1000 / FRAME_RATE);
  }, []);

  return (
    <div className="app">
      <div id={SCORE_ID} className="score">
        0
      </div>
      <canvas
        id={CANVAS_ID}
        width={CANVAS_SIZE}
        height={CANVAS_SIZE}
        className="canvas"
      />
    </div>
  );
};

export default App;
