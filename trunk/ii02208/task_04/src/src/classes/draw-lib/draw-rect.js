export const drawRect = (
  context,
  borderWidth,
  borderColor,
  fillColor,
  x1,
  y1,
  x2,
  y2
) => {
  context.strokeStyle = borderColor;
  context.lineWidth = borderWidth;
  context.fillStyle = fillColor;
  context.beginPath();
  context.rect(x1, y1, x2 - x1, y2 - y1);
  context.fill();
  context.stroke();
};
