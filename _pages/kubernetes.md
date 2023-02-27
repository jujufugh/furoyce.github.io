---
permalink: /cloud/k8s/    
title: "Kubernetes"
author_profile: false
classes: wide
sidebar:
    nav: "docs"
---

{% for tag in site.tags %}
{% if tag[0] == "Kubernetes" %}
  <!--<h3>{{ tag[0] }}</h3>-->
  <ul>
    {% for post in tag[1] %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endif %}
{% endfor %}