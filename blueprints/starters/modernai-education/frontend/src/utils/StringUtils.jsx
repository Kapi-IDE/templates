// Utility function to capitalize the first letter of each word
export function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
}

// Utility function to format the user's name and role
export function formatUserInfo(firstName, lastName, role) {
  const formattedName = `${capitalize(firstName)} ${capitalize(
    lastName.charAt(0)
  )}.`;
  const formattedRole = capitalize(role);
  return { formattedName, formattedRole };
}
