import React from "react";
import DiscordWidget from "./DiscordWidget"; // Adjust the import path as necessary

const Discord = () => {
  const serverId = "1122269242373459968";

  return (
    <div>
      <h2>Join the Mitra Discord Community!</h2>
      <DiscordWidget serverId={serverId} />
    </div>
  );
};

export default Discord;
