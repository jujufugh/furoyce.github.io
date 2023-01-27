---
permalink: /oracle/maa/
title: "Maximum Availability Architecture References"
author_profile: false
classes: wide
sidebar:
    nav: "docs"
---

{% for tag in site.tags %}
{% if tag[0] == "MAA" %}
  <!--<h3>{{ tag[0] }}</h3>-->
  <ul>
    {% for post in tag[1] %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endif %}
{% endfor %}