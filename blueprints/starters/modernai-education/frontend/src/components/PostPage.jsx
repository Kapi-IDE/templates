import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Heading, Box, Text } from "@chakra-ui/react";
import { GET_POST } from "../Constants";

const PostPage = () => {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await fetch(GET_POST(id));
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const postData = await response.json();
        setPost(postData);
      } catch (error) {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchPost();
  }, [id]);

  const processHtmlContent = (htmlContent) => {
    let processedContent = htmlContent.replace(/<br\s*\/?>/gi, "\n");
    processedContent = processedContent.replace(/<[^>]+>/g, "");
    return processedContent;
  };

  const HtmlContentRenderer = ({ htmlContent }) => {
    const processedContent = processHtmlContent(htmlContent);
    return processedContent.split("\n").map((line, index) => (
      <Text key={index} fontSize="lg" lineHeight="tall">
        {line}
      </Text>
    ));
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!post) {
    return <div>Post not found.</div>;
  }

  return (
    <Container maxWidth="1200px" py={8}>
      <Heading as="h1" mb={4}>
        {post.title}
      </Heading>
      <Box>{HtmlContentRenderer({ htmlContent: post.content })}</Box>
    </Container>
  );
};

export default PostPage;
