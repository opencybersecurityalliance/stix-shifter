import React from "react";
import { useSelector, useDispatch } from "react-redux";
import styles from "./from_stix.module.scss";
import MappingItem from "./MappingItem";
import MappingsFilterBar from "./MappingsFilterBar";
import { filterMappingFieldsForValue } from "./utils";
import { clearMappings } from "../../store/actions/from_stix";

const Mapping = () => {
  const dispatch = useDispatch();
  const stixMapping = useSelector((state) => state.fromStix.stixMapping);
  const fieldMappingFilter = useSelector(
    (state) => state.fromStix.fieldMappingFilter
  );

  return (
    <>
      <div className="bx--row">
        <div className="bx--col">
          <h4 className="section-title">
            {Object.keys(stixMapping).length} Total Fields{" "}
            <span
              onClick={() => {
                dispatch(clearMappings());
              }}
              className={styles.mappings_clear__btn}
            >
              (Clear)
            </span>
          </h4>
        </div>
      </div>

      <div className="bx--row">
        <div className="bx--col">
          <MappingsFilterBar />
        </div>
      </div>
      <div className="bx--row">
        <div
          className={`bx--col ${styles.full_height__col} ${styles.mapping__col}`}
        >
          {Object.keys(
            filterMappingFieldsForValue(stixMapping, fieldMappingFilter)
          ).map((o) => (
            <MappingItem key={o} title={o} />
          ))}
        </div>
      </div>
    </>
  );
};

export default Mapping;
