import React from "react";
import styles from "./to_stix.module.scss";

const StatisticObject = ({ fieldsCount, objectsCount, sum, type }) => {
  const objectsStatistics = (fieldsCount / sum) * 100;

  return (
    <div className="bx--col">
      <div className="bx--label-description">{type} STIX fields</div>
      <div className={styles.coverage_percent}>
        {sum === 0 ? 0 : Math.round(objectsStatistics * 100) / 100}%
      </div>
      <div className={styles.coverage_count}>{fieldsCount} STIX fields</div>
      <div className={styles.coverage_count}>{objectsCount} STIX objects</div>
    </div>
  );
};

export default React.memo(StatisticObject);
