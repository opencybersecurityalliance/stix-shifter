export const isValidCustomStixField = (customField) => {
  const re = /(^\S+:+\S+$)/;
  return re.test(customField);
};
