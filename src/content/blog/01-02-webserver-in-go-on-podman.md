---
title: '01-02 Webserver in Go on Podman'
description: 'Webserver in Go on Podman'
pubDate: 'August 07 2023'
heroImage: '/blog-placeholder-4.jpg'
githubName: '01-02-Webserver-in-Go-on-Podman'
---

# What is this about?

This is about use of external CSS files, e.g. styles/styles.css and external Javascript files, e.g. scripts/main.js in a HTML 5 Page.

# explanation

To use this external files you need a Webserver. A big one? No a very small one: A Go implemented Webserver. It is a one-line implementation in Go.

Why i need a webserver for external files?

If you try open jour HTML 5 file local over the file:/// schema, and in this HTML 5 file are external files your browser resolve them also local over the file:/// schema.

This let the broswer gives you CORS errors.

For example: Reason: CORS request not HTTP.

CORS (Cross-Origin Resource Sharing) is a security system about the origin of external files. This work only with https:/// schema or http:/// schema.

This is where the web server comes into play.

# Well and what does podman mean?

Podman is a open source container tool. I embed the go webserver in a Dockerfile and let it run in Podman. And more there is a Podman Desktop tool, it is an open source graphical tool to work with containers. The Project readme.md explains all in detail.

# explore

and run your first webproject with externals files.

# travel to, explore

and run your first webproject with externals files.

[Git Repo roebi/01-02-Webserver-in-Go-on-Podman](https://github.com/roebi/01-02-Webserver-in-Go-on-Podman)

remark: You can make a own repository from this template and then work in your own repository.
