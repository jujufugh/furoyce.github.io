---
title: "Recent Posts"
permalink: /posts/
layout: archive
author_profile: false
classes: wide
sidebar:
    nav: "docs"
---

{% for post in site.posts %}
  {% unless post.hidden %}
    {% include archive-single.html %}
  {% endunless %}
{% endfor %}
