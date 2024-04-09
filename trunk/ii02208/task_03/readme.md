# Лабораторная работа №3

### Тема

Разработка web-интерфейса

### Задание

Создание сайта по заданной тематике. Сайт представляет собой макет высокого уровня без функциональной части. Реализовать возможность демонстрации работы сайта, заполняя поля необходимой информацией и демонстрируя переходы между страницами сайта.
Сайт для прослушивания музыки (spotify)

### Результат работы

![результат](./images/site.png)

### Код программы

```
function App() {
  const [record, setRecord] = useState;
  const [audio, setAudio] = useState;

  return (
    <div>
      <img />
      <div className={styles.wrapper}>
        <AudioPlayer />
        <div className={styles.recordWrap}>
          <RecordPreview />
          <RecordsAudioList />
        </div>
      </div>
      <RecordsList />
    </div>
  );
}

export default App;
```
