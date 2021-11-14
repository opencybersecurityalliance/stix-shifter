import React, { useMemo } from "react";
import { useSelector } from "react-redux";
import styles from "./to_stix.module.scss";
import { getDataForStatistics } from "./utils";
import StatisticObject from "./StatisticObject";

const Statistics = ({ stixMapping }) => {
  const stixFields = useSelector((state) => state.stix.stixFields);
  const stixTypesSet = useMemo(
    () => new Set(Object.values(stixFields).map((field) => field.type)),
    [stixFields]
  );
  const [
    officialFieldsCount,
    customFieldsCount,
    officialObjectsCount,
    customObjectsCount,
  ] = getDataForStatistics(stixMapping, stixTypesSet);

  const sum = officialFieldsCount + customFieldsCount;

  return (
    <>
      <div className="bx--row">
        <div className={"bx--col"}>
          <h4 className="section-title">Official VS Custom STIX fields</h4>
        </div>
      </div>

      <div className="bx--row" style={{ marginBottom: ".75rem" }}>
        <div className={`bx--col ${styles.statistics__col}`}>
          <div className="bx--row">
            <StatisticObject
              fieldsCount={officialFieldsCount}
              objectsCount={officialObjectsCount}
              sum={sum}
              type={"Official"}
            />
          </div>
        </div>
        <div className={`bx--col ${styles.statistics__col}`}>
          <div className="bx--row">
            <StatisticObject
              fieldsCount={customFieldsCount}
              objectsCount={customObjectsCount}
              sum={sum}
              type={"Custom"}
            />
          </div>
        </div>
      </div>
    </>
  );
};

export default Statistics;
