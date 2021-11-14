import React, { useState } from "react";
import { useSelector } from "react-redux";
import { Link } from "react-scroll";
import styles from "./to_stix.module.scss";
import StickyBox from "react-sticky-box";
import { isActiveObject } from "./utils";

const Minimap = ({ isStix }) => {
  const mappingObjects = isStix ? "stixMapping" : "metadataMapping";
  const mapping = useSelector((state) => state.toStix[mappingObjects]);
  const [activeObject, setActiveObject] = useState("");

  return (
    <div className="bx--col-sm-1">
      <StickyBox offsetTop={70}>
        <div className={styles.Sticky__Box}>
          <h4 className="section-title" style={{ marginLeft: "1rem" }}>
            Objects Map
          </h4>
          <div className={styles.minimap}>
            {Object.keys(mapping).map((o) => {
              return (
                <div key={`link_${o}`} id={`link_${o}`}>
                  <Link
                    to={`${o}`}
                    spy={true}
                    smooth={true}
                    offset={-100}
                    onSetActive={() => setActiveObject(o)}
                  >
                    <div
                      className={`${styles.minimap__tile} 
                        ${
                          isActiveObject(o, activeObject)
                            ? styles.minimap__activeTile
                            : ""
                        }`}
                    >
                      {o}
                    </div>
                  </Link>
                </div>
              );
            })}
          </div>
        </div>
      </StickyBox>
    </div>
  );
};

export default Minimap;
