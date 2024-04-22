import { useState } from "react";
import { data } from "../constants/data";
import styles from "./App.module.css";
import { AudioPlayer } from "../components/audio-player/audio-player";
import { RecordsList } from "../components/records-list/records-list";
import { RecordsAudioList } from "../components/record-audio-list/record-audio-list";
import { RecordPreview } from "../components/record-preview/record-preview";
import DisclaimerImage from "../assets/disclaimer.png";

function App() {
  const [record, setRecord] = useState(data.powvawe);
  const [audio, setAudio] = useState({
    name: record.trackList[0].name,
    duration: record.trackList[0].duration,
    image: record.image,
    recordName: record.name,
  });

  return (
    <div className={styles.content} style={{ background: record.color }}>
      <img
        src={DisclaimerImage}
        width={80}
        style={{ position: "fixed", bottom: 40, left: 40 }}
        alt=""
      />
      <div className={styles.wrapper}>
        <AudioPlayer
          name={audio.name}
          duration={audio.duration}
          image={audio.image}
          recordName={audio.recordName}
        />
        <div className={styles.recordWrap}>
          <RecordPreview
            image={record.image}
            date={record.date}
            length={record.trackList.length}
            duration={record.trackList.reduce(
              (time, audio) => time + audio.duration,
              0
            )}
            name={record.name}
          />
          <RecordsAudioList
            trackList={record.trackList}
            image={record.image}
            setAudio={(index) =>
              setAudio({
                name: record.trackList[index].name,
                duration: record.trackList[index].duration,
                image: record.image,
                recordName: record.name,
              })
            }
          />
        </div>
      </div>
      <RecordsList
        recordPreviews={Object.entries(data)
          .sort((a, b) => b[1].order - a[1].order)
          .reduce((recordPreviews, record) => {
            const recordPreview = {
              name: record[1].name,
              image: record[1].image,
              date: record[1].date,
              key: record[0],
            };
            recordPreviews.push(recordPreview);
            return recordPreviews;
          }, [])}
        setRecord={(key) => setRecord(data[key])}
      />
    </div>
  );
}

export default App;
