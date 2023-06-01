---
title: Gradient optimization for inverse kinematics
categories:
- engineering
layout: post
description: Inverse kinematics is one of the hardest problems in robotics. Given desired goal position and orientation for an end-effector, inverse kinematics seeks to find a suitable series of joint configurations to meet that goal. In this paper, we develop a forward kinematics model in Python and apply gradient-based methods using automatic differentiation to develop an inverse kinematics model of an arbitrary $n$-joint robot arm. We evaluate the performance of standard gradient descent against Nesterov Momentum gradient descent. We conclude with a discussion of the limitations of our 2D model and areas for extension to gain more fidelity with real-world robots.
image: "https://github.com/p13i/p13i.github.io/assets/13140065/7bbaea7b-892e-4a20-baa3-d1ef46c8e000"
downloads:
- name: "📜 Report PDF"
  url: https://github.com/p13i/p13i.github.io/files/11621390/AA222_project_final_report.pdf
pages_images:
- https://github.com/p13i/p13i.github.io/assets/13140065/10d8f49c-73af-41fb-9efd-0231a439d218
- https://github.com/p13i/p13i.github.io/assets/13140065/b03ceb32-0af6-4f01-9fa8-39a501787ef7
- https://github.com/p13i/p13i.github.io/assets/13140065/58ce9bd9-61c2-4c03-906c-f4fd17b22931
- https://github.com/p13i/p13i.github.io/assets/13140065/01322cc0-54e4-4879-9e05-4070fc971690
---

{% for img in page.pages_images %}
{% include _post_image.html src=img %}
{% endfor %}
