/**
 * MDX Content Processing Utilities
 *
 * Features:
 * - Parse frontmatter from MDX files
 * - Load blog posts from filesystem
 * - Sort by date
 * - Generate slugs
 */

import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

// Posts directory
const postsDirectory = path.join(process.cwd(), 'posts');

export interface Post {
  slug: string;
  title: string;
  date: string;
  description: string;
  author?: string;
  tags?: string[];
  coverImage?: string;
  content: string;
}

export interface PostMetadata {
  slug: string;
  title: string;
  date: string;
  description: string;
  author?: string;
  tags?: string[];
  coverImage?: string;
}

/**
 * Get all post slugs (filenames without extension)
 */
export function getAllPostSlugs(): string[] {
  try {
    const fileNames = fs.readdirSync(postsDirectory);
    return fileNames
      .filter((fileName) => fileName.endsWith('.mdx') || fileName.endsWith('.md'))
      .map((fileName) => fileName.replace(/\.(mdx|md)$/, ''));
  } catch (error) {
    console.warn('Posts directory not found, returning empty array');
    return [];
  }
}

/**
 * Get post data by slug
 */
export function getPostBySlug(slug: string): Post {
  const realSlug = slug.replace(/\.mdx?$/, '');

  // Try .mdx first, then .md
  let fullPath = path.join(postsDirectory, `${realSlug}.mdx`);
  if (!fs.existsSync(fullPath)) {
    fullPath = path.join(postsDirectory, `${realSlug}.md`);
  }

  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const { data, content } = matter(fileContents);

  return {
    slug: realSlug,
    title: data.title || 'Untitled',
    date: data.date || new Date().toISOString(),
    description: data.description || '',
    author: data.author,
    tags: data.tags || [],
    coverImage: data.coverImage,
    content,
  };
}

/**
 * Get all posts metadata (sorted by date, newest first)
 */
export function getAllPosts(): PostMetadata[] {
  const slugs = getAllPostSlugs();
  const posts = slugs
    .map((slug) => {
      const post = getPostBySlug(slug);
      return {
        slug: post.slug,
        title: post.title,
        date: post.date,
        description: post.description,
        author: post.author,
        tags: post.tags,
        coverImage: post.coverImage,
      };
    })
    .sort((a, b) => {
      // Sort by date descending
      return new Date(b.date).getTime() - new Date(a.date).getTime();
    });

  return posts;
}

/**
 * Get posts by tag
 */
export function getPostsByTag(tag: string): PostMetadata[] {
  const allPosts = getAllPosts();
  return allPosts.filter((post) => post.tags?.includes(tag));
}

/**
 * Get all unique tags
 */
export function getAllTags(): string[] {
  const allPosts = getAllPosts();
  const tags = new Set<string>();

  allPosts.forEach((post) => {
    post.tags?.forEach((tag) => tags.add(tag));
  });

  return Array.from(tags).sort();
}

/**
 * Format date for display
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

/**
 * Calculate reading time
 */
export function getReadingTime(content: string): number {
  const wordsPerMinute = 200;
  const wordCount = content.split(/\s+/).length;
  return Math.ceil(wordCount / wordsPerMinute);
}
