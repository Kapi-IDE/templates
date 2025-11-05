import React from "react";

const DiscordWidget = ({ serverId }) => {
  const src = `https://discord.com/widget?id=${serverId}&theme=dark`; // You can change "dark" to "light" depending on your preference

  return (
    <iframe
      src={src}
      width="100%"
      height="600px" // Adjust the height as needed
      allowTransparency="true"
      frameborder="0"
      sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"
      title="Discord"
      style={{ border: "none", borderRadius: "4px" }} // Style as needed
    ></iframe>
  );
};

export default DiscordWidget;
