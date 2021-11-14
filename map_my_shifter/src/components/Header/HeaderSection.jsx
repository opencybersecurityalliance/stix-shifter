import React from "react";
import { Link } from "@carbon/ibm-security";
import styles from "./headerSection.module.scss";
import { useHistory } from "react-router-dom";

const HeaderSection = () => {
  const history = useHistory();
  const goTo = (link) => {
    history.push(link);
  };

  return (
    <div className="bx--row">
      <div className="bx--col">
        <div className="bx--row" style={{ paddingLeft: "1rem" }}>
          <Link onClick={() => goTo("/")} className={styles.tile__btn}>
            Map My Shifter
          </Link>
          <div className={styles.tile__separator}>|</div>
          <Link onClick={() => goTo("/About")} className={styles.tile__btn}>
            About
          </Link>
          <div className={styles.tile__separator}>|</div>
          <Link onClick={() => goTo("/from_stix")} className={styles.tile__btn}>
            From STIX
          </Link>
          <div className={styles.tile__separator}>|</div>
          <Link onClick={() => goTo("/to_stix")} className={styles.tile__btn}>
            To STIX
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HeaderSection;
