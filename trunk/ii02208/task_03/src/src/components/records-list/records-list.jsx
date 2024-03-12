import styles from "./records-list.module.css";
import PropTypes from "prop-types";

export function RecordsList({ recordPreviews, setRecord }) {
  RecordsList.propTypes = {
    recordPreviews: PropTypes.array,
    setRecord: PropTypes.func,
  };

  return (
    <div className={styles.wrap}>
      {recordPreviews.map((record) => (
        <button
          className={styles.recordItemContent}
          key={record.key}
          onClick={() => setRecord(record.key)}
        >
          <img
            draggable={false}
            className={styles.image}
            src={record.image}
            width={180}
            height={180}
            alt={record.name}
          />
          <div className={styles.name}>{record.name}</div>
          <div className={styles.date}>{record.date}</div>
        </button>
      ))}
    </div>
  );
}
