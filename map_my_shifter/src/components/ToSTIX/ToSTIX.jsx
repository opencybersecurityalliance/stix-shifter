import React from "react";
import { useSelector } from "react-redux";
import MappingTabs from "./MappingTabs";
import Statistics from "./Statistics";

const ToSTIX = () => {
  const stixMapping = useSelector((state) => state.toStix.stixMapping);

  return (
    <>
      <div className="bx--grid">
        <div className="bx--row">
          <MappingTabs />
          <div className="bx--col-sm-1">
            <div className="bx--row">
              <div className="bx--col-sm-4">
                <Statistics stixMapping={stixMapping} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ToSTIX;
