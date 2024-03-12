import styles from "./record-audio-list.module.css";

export function RecordsAudioList({ trackList=[], setAudio=null, image=null }) {
  return (
    <div className={styles.wrap}>
      {trackList.map((audio, index) => (
        <div
          className={styles.audioContent}
          key={index}
          onClick={() => setAudio && setAudio(index)}
        >
          <div className={styles.audioInfoWrap}>
            <div className={styles.number}>{index + 1}.</div>
            {image && <img
              draggable={false}
              className={styles.image}
              src={image}
              width={40}
              height={40}
              alt={index}
            />}
            <div className={styles.name}>{audio.name}</div>
          </div>
          <div className={styles.duration}>
            {Math.round(audio.duration / 60)}:
            {String(Math.round(audio.duration % 60)).length < 2
              ? "0" + Math.round(audio.duration % 60)
              : Math.round(audio.duration % 60)}
          </div>
        </div>
      ))}
    </div>
  );
}
