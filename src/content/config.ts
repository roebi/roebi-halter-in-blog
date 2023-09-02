import { defineCollection, z } from "astro:content";

const blog = defineCollection({
  // Type-check frontmatter using a schema
  type: "content",
  schema: z.object({
    title: z.string(),
    description: z.string(),
    // Transform string to Date object
    pubDate: z
      .string()
      .or(z.date())
      .transform((val) => new Date(val)),
    updatedDate: z
      .string()
      .optional()
      .transform((str) => (str ? new Date(str) : undefined)),
    heroImage: z.string().optional(),
    githubName: z.string(), // ,
    // the raw data does NOT have githubTopics // we get them dynamic from github
    // githubTopics: z.array(z.string()) // .optional() return String | undefined
  }),
});

export const collections = {
  blog: blog,
};
