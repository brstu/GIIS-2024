# Лабораторная работа №4

### Тема

Разработка игры

### Задание

Создать игру змейка

### Результат работы

![результат](./images/Snake-demo.gif)

### Код программы

```tsx
const App = () => {
  useEffect(() => {
    setInterval(() => game.eventLoop(), 1000 / FRAME_RATE);
  }, []);

  return (
    <div className="app">
      <div id={SCORE_ID}>0</div>
      <canvas id={CANVAS_ID} />
    </div>
  );
};
```
