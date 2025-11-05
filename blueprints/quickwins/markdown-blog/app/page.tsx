import Link from 'next/link';
import { getAllPosts, formatDate } from '@/lib/mdx';

export default function HomePage() {
  const posts = getAllPosts();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-4xl mx-auto px-4 py-16">
        {/* Header */}
        <header className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            My Blog
          </h1>
          <p className="text-xl text-gray-600">
            Thoughts, stories, and ideas
          </p>
        </header>

        {/* Posts List */}
        <div className="space-y-8">
          {posts.length === 0 ? (
            <div className="text-center py-16">
              <p className="text-gray-500 text-lg">
                No posts yet. Create your first post in the <code className="bg-gray-100 px-2 py-1 rounded">posts/</code> directory!
              </p>
              <p className="text-gray-400 mt-4">
                Example: <code className="bg-gray-100 px-2 py-1 rounded text-sm">posts/hello-world.mdx</code>
              </p>
            </div>
          ) : (
            posts.map((post) => (
              <article
                key={post.slug}
                className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden"
              >
                <Link href={`/blog/${post.slug}`}>
                  {post.coverImage && (
                    <div className="w-full h-48 bg-gray-200 overflow-hidden">
                      <img
                        src={post.coverImage}
                        alt={post.title}
                        className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                  )}
                  <div className="p-6">
                    <div className="flex items-center text-sm text-gray-500 mb-3">
                      <time dateTime={post.date}>
                        {formatDate(post.date)}
                      </time>
                      {post.author && (
                        <>
                          <span className="mx-2">·</span>
                          <span>{post.author}</span>
                        </>
                      )}
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition-colors">
                      {post.title}
                    </h2>
                    <p className="text-gray-600 mb-4">
                      {post.description}
                    </p>
                    {post.tags && post.tags.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {post.tags.map((tag) => (
                          <span
                            key={tag}
                            className="inline-block bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </Link>
              </article>
            ))
          )}
        </div>

        {/* Footer */}
        <footer className="mt-16 pt-8 border-t border-gray-200 text-center text-gray-500">
          <p>Built with Next.js + MDX</p>
        </footer>
      </div>
    </div>
  );
}
