import { useMemo, useState } from "react";
import styles from "./audio-player.module.css";
import {
  StepBackwardOutlined,
  StepForwardOutlined,
  PauseOutlined,
  CaretRightOutlined,
  SoundOutlined,
  MutedOutlined,
} from "@ant-design/icons";
import Icon from "@ant-design/icons/lib/components/Icon";

export function AudioPlayer({ name, duration, image, recordName, style }) {
  const [time, setTime] = useState((duration / 3) * 1.34);
  const [isPause, setIsPause] = useState(false);
  const [volume, setVolume] = useState(50);

  const timeValue = useMemo(() => {
    const minTime = Math.round(time / 60);
    const secTime = String(Math.round(time % 60));
    const minDuration = Math.round(duration / 60);
    const secDuration = String(Math.round(duration % 60));
    return (
      minTime +
      ":" +
      (secTime.length < 2 ? 0 + secTime : secTime) +
      " - " +
      minDuration +
      ":" +
      (secDuration.length < 2 ? 0 + secDuration : secDuration)
    );
  }, [duration, time]);

  return (
    <div className={styles.wrapper} style={style}>
      <div className={styles.content}>
        <Icon component={StepBackwardOutlined} className={styles.button} />
        <Icon
          component={isPause ? CaretRightOutlined : PauseOutlined}
          className={styles.button}
          onClick={() => setIsPause(!isPause)}
        />
        <Icon component={StepForwardOutlined} className={styles.button} />
        <img draggable={false} className={styles.image} src={image} alt="" />
        <div className={styles.audioInfoWrap}>
          <div className={styles.titleWrap}>
            <div className={styles.name}>
              {recordName} - {name}
            </div>
            <div className={styles.duration}>{timeValue}</div>
          </div>
          <div className={styles.timeLineWrap}>
            <div
              className={styles.timeLineValue}
              style={{ width: Math.round((time / duration) * 100) + "%" }}
            />
          </div>
        </div>
        <Icon
          component={volume === 0 ? MutedOutlined : SoundOutlined}
          className={styles.button}
          onClick={() => (volume > 0 ? setVolume(0) : setVolume(100))}
        />
        <div className={styles.volumeWrap}>
          <div className={styles.volumeValue} style={{ width: volume + "%" }} />
        </div>
        <div className={styles.volume}>{volume}%</div>
      </div>
    </div>
  );
}
