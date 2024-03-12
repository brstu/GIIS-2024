import styles from "./record-preview.module.css";

function getLengthName(length) {
  if (length % 10 === 1) {
    return "трек";
  }
  if (length % 10 > 1 && length % 10 < 5) {
    return "трека";
  }
  return "треков";
}

export function RecordPreview({ image, name, duration, date, length }) {
  return (
    <div className={styles.wrap}>
      <img draggable={false} className={styles.bgImage} src={image} alt="" />
      <div className={styles.content}>
        <img
          draggable={false}
          className={styles.image}
          src={image}
          width={300}
          height={300}
          alt={name}
        />
        <div className={styles.info}>
          <div className={styles.name}>{name}</div>
          <div className={styles.date}>{date}</div>
          <div className={styles.time}>
            {Math.round(duration / 60)}:
            {String(Math.round(duration % 60)).length < 2
              ? "0" + Math.round(duration % 60)
              : Math.round(duration % 60)}
            {" мин, "}
            {length + " "}
            {getLengthName(length)}
          </div>
        </div>
      </div>
    </div>
  );
}
