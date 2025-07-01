import { getCollection } from "astro:content";
import type { APIRoute } from "astro";

export const GET: APIRoute = async () => {
    const blogPosts = await getCollection("blog"); // adjust "blog" to your collection name
    const content = `# roebi's blog\n
    ${blogPosts
            .map(
                (blogPost) =>
                    `# ${blogPost.data.title}\n\n
                https://roebi.github.io/roebi-halter-in-blog/blog/${blogPost.slug}.md \n
                ${blogPost.data.description} \n
                  ${blogPost.body}
                }`
            )
            .join("\n\n")}`;
    return new Response(content, {
        headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
};
