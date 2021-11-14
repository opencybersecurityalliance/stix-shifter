import React from "react";
import logo from "./logo-no-bg.png";
import { ClickableTile } from "@carbon/ibm-security";
import styles from "./welcome.module.scss";
import { useHistory } from "react-router-dom";

const Welcome = () => {
  const history = useHistory();
  const handleClickableTile = (link) => {
    history.push(link);
  };

  return (
    <>
      <div className="bx--grid">
        <div className="bx--row">
          <div className="bx--col">
            <img src={logo} alt="Logo" width={300} />
          </div>
        </div>
        <div className="bx--row">
          <div className="bx--col">
            <p>
              This tool is used for generating mapping file for `STIX-Shifter`
              project
            </p>
          </div>
        </div>

        <div className="bx--row">
          <div className="bx--col-sm-2">
            <ClickableTile
              handleClick={() => handleClickableTile("/from_stix")}
              className={styles.tile__btn}
            >
              Generate "From STIX" File
            </ClickableTile>
          </div>
          <div className="bx--col-sm-2">
            <ClickableTile
              handleClick={() => handleClickableTile("/to_stix")}
              className={styles.tile__btn}
            >
              Generate "To STIX" File
            </ClickableTile>
          </div>
        </div>
      </div>
    </>
  );
};

export default Welcome;
