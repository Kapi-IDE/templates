import React, { useEffect, useState } from "react";
import axios from "axios";

import { BASE_TITLE, GET_RECORDING, RECORDING_PUBLIC_URL } from "../Constants";
import { Box, VStack, Icon, useColorModeValue } from '@chakra-ui/react';
import { HStack, useDisclosure } from "@chakra-ui/react";
import { Button } from "@chakra-ui/react";

import { FiChevronLeft, FiChevronRight } from 'react-icons/fi';

import ReactPlayer from "react-player";

const TreeViewer = ({ content, onClickHandler }) => {
  // Check if the object is null or undefined
  if (!content) {
    return <div>Object is null or undefined</div>;
  }

  const renderTree = (obj, depth = 0) => {
    const indent = {
      paddingLeft: `${depth * 20}px`,
    };

    return (
      <ul style={{ listStyleType: "none", padding: 0 }}>
        {Object.entries(obj).map(([key, value]) => {
          const isVideoItem =
            typeof value === "object" &&
            "filename" in value &&
            "blob_url" in value;
          return (
            <li key={key}>
              <div style={indent}>
                {!!isNaN(key) && <strong>{key}: </strong>}{" "}
                {/* Render key if it's not a number */}
                {typeof value !== "object" && <span>{value}</span>}
                {typeof value === "object" &&
                  !isVideoItem &&
                  renderTree(value, depth + 1)}
                {typeof value === "object" && isVideoItem && (
                  <button onClick={() => onClickHandler(value)}>
                    {value.filename}
                  </button>
                )}
              </div>
            </li>
          );
        })}
      </ul>
    );
  };
  return (
    <div>
      <div>{renderTree(content)}</div>
    </div>
  );
};

const VideoViewer = ({ video }) => {
  const [publicUrlApi, setPublicUrlApi] = useState({
    state: "Loading",
    url: "",
  });

  useEffect(() => {
    const fetchPublicUrl = async () => {
      try {
        const response = await axios.post(RECORDING_PUBLIC_URL, {
          blob_url: video.blob_url,
          // expiry_time_hrs: 4.0,
        });
        setPublicUrlApi({ state: "Success", url: response.data });
      } catch (error) {
        console.error("Error fetching video", error);
        setPublicUrlApi((data) => ({ ...data, state: "Error" }));
      }
    };

    video.blob_url && fetchPublicUrl();
  }, [video]);

  return (
    <div>
      {!video.blob_url && "Select a video"}
      {video.blob_url && publicUrlApi.state === "Loading" && "Loading..."}
      {publicUrlApi.state === "Error" && "Error In Loading Data"}
      {publicUrlApi.state === "Success" && (
        <div
          className="video-viewer"
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <ReactPlayer
            url={publicUrlApi.url}
            controls={true}
            width="100%"
            height="100%"
            config={{
              file: {
                attributes: {
                  onContextMenu: (e) => e.preventDefault(),
                  controlsList: "nodownload",
                },
              },
            }}
          />
        </div>
      )}
    </div>
  );
};

const CourseContentBar = ({ isOpen, onToggle, videoUrlApi, clickHander }) => {
  const bgColor = useColorModeValue('gray.200', 'gray.800');
  return (
    <Box
      w={isOpen ? '500px' : '0'}
      bg={bgColor}
      transition="width 0.5s ease"
      boxShadow="lg"
      position="relative"  // Set position to relative
    >
      <VStack spacing={4} mt={8} align="stretch">
        {/* Move the IconButton to the end of the VStack */}
        <Button
          aria-label="Toggle sidebar"
          onClick={onToggle}
          borderRadius={isOpen ? "5%" : "50%" }
        >
          {isOpen ? 
            <Box>Course Content <Icon as={FiChevronRight}/></Box> 
              : 
            <Icon as={FiChevronLeft}/>}
        </Button>
        { isOpen && <Box>
          <h1>List of Videos</h1>
          <ul>
            {videoUrlApi.state === "Error" && "Error In Loading Data"}
            {videoUrlApi.state === "Loading" && "Loading..."}
            {videoUrlApi.state === "Success" && ( // When we get the data
              <TreeViewer content={videoUrlApi.data} onClickHandler={clickHander} />
            )}
          </ul>
        </Box>}
      </VStack>
    </Box>
  );
};

function Recordings() {
  const [videoUrlApi, setVideoUrlApi] = useState({
    state: "Loading",
    data: [],
  });
  const { isOpen: isSidebarClosed, onToggle:onToggleSidebar} = useDisclosure({ defaultIsOpen:true });
  const [videoItem, setVideoItem] = useState({
    filename: "File Not Set",
    blob_url: null,
  });

  useEffect(() => {
    document.title = "Recording | " + BASE_TITLE;

    const fetchVideoUrl = async () => {
      try {
        const response = await axios.get(GET_RECORDING);
        setVideoUrlApi({ state: "Success", data: response.data });
      } catch (error) {
        console.error("Error fetching video", error);
        setVideoUrlApi((data) => ({ ...data, state: "Error" }));
      }
    };

    fetchVideoUrl();
  }, []);

  const clickHander = (item) => {
    setVideoItem(item);
  };

  return (
    <div>
      <HStack spacing={"45px"} align={"start"}>
        <CourseContentBar isOpen={isSidebarClosed} onToggle={onToggleSidebar} videoUrlApi={videoUrlApi} clickHander={clickHander} />
        <VideoViewer video={videoItem} />
      </HStack>
    </div>
  );
}

export default Recordings;
