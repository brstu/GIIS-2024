import styles from "./record-audio-list.module.css";
import PropTypes from 'prop-types';

export function RecordsAudioList({ trackList, setAudio, image }) {

  RecordsAudioList.propTypes = {
    trackList: PropTypes.array,
    setAudio: PropTypes.func,
    image: PropTypes.string,
  };

  return (
    <div className={styles.wrap}>
      {trackList.map((audio, index) => (
        <div
          className={styles.audioContent}
          key={index}
          onClick={() => setAudio(index)}
        >
          <div className={styles.audioInfoWrap}>
            <div className={styles.number}>{index + 1}.</div>
            <img
              draggable={false}
              className={styles.image}
              src={image}
              width={40}
              height={40}
              alt={index}
            />
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
