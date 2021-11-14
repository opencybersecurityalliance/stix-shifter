import React, { useEffect } from "react";
import "@carbon/ibm-security/css/index.min.css";
import { Provider } from "react-redux";
import store from "./store/store";
import FromSTIX from "./components/FromSTIX/FromSTIX";
import ToSTIX from "./components/ToSTIX/ToSTIX";
import { changeStixVersion } from "./store/actions/stix";
import { STIX_VERSION } from "./global/constants";
import { loadJsonFromDisk as loadFromStixJsonFromDisk } from "./components/FromSTIX/utils";
import { loadJsonFromDisk as loadToStixJsonFromDisk } from "./components/ToSTIX/utils";
import { updateMappingsFromFile as createFromStixStateMapping } from "./store/actions/from_stix";
import { updateMappingsFromFile as createToStixStateMapping } from "./store/actions/to_stix";
import { stateMappingToShifterMapping as createFromStixShifterMapping } from "./components/FromSTIX/utils";
import { stateMappingToShifterMapping as createToStixShifterMapping } from "./components/ToSTIX/utils";
import { saveJsonToDisk } from "./components/STIX/utils";
import * as serviceWorker from "./serviceWorker";

export const FromStix = {
  Mapping: ({ StixVersion }) => {
    useEffect(() => {
      const version = StixVersion ? StixVersion : "V_2_0";
      store.dispatch(changeStixVersion(STIX_VERSION[version]));
      // eslint-disable-next-line
    }, [StixVersion]);
    return (
      <Provider store={store}>
        <FromSTIX />
      </Provider>
    );
  },
  Export: (fileName) => {
    const fromStixMapping = store.getState().fromStix.stixMapping;
    const FromStixShifterMapping =
      createFromStixShifterMapping(fromStixMapping);
    return saveJsonToDisk(fileName, FromStixShifterMapping);
  },
  Import: (mapping) => {
    const stixMapping = loadFromStixJsonFromDisk(mapping)[0];
    store.dispatch(createFromStixStateMapping(stixMapping));
  },
};

export const ToStix = {
  Mapping: ({ StixVersion }) => {
    useEffect(() => {
      const version = StixVersion ? StixVersion : "V_2_0";
      store.dispatch(changeStixVersion(STIX_VERSION[version]));
    }, [StixVersion]);
    return (
      <Provider store={store}>
        <ToSTIX />
      </Provider>
    );
  },
  Export: (fileName) => {
    const toStixMapping = store.getState().toStix.stixMapping;
    const toStixMetadataMapping = store.getState().toStix.metadataMapping;
    const ToStixShifterMapping = createToStixShifterMapping(
      toStixMapping,
      toStixMetadataMapping
    );
    return saveJsonToDisk(fileName, ToStixShifterMapping);
  },
  Import: (mapping) => {
    const [stixMapping, metadataMapping] = loadToStixJsonFromDisk(mapping);
    store.dispatch(createToStixStateMapping(stixMapping, metadataMapping));
  },
};

serviceWorker.unregister();
