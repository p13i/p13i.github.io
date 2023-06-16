---
title: Jellyfish
date: 2019-06-09 00:00:00 Z
categories:
  - design
tags:
  - cinema-4d
  - octane-render
  - graphic-design
  - simulation
  - hair
  - adobe-illustrator
  - adobe-after-effects
  - 3d-modeling
layout: post
author: Pramod Kotipalli
description: Modeling, rigging, and animating a bioluminescent jellyfish
subcategories:
  - design
downloads:
  - name: "\U0001F4F1 iPhone X (2436-by-1125 - 2.5 MB)"
    url: "/assets/images/2019-06-09-jellyfish/downloads/jellyfish-iphone-x.jpg"
  - name: "\U0001F5A5️ Desktop (2560-by-1600 - 3.7 MB)"
    url: "https://drive.google.com/open?id=1Q_7Pam_uwsWqCJdrubYEKhIw_GUajxqD"
  - name: "\U0001F5BC️ Full (4096-by-4096, 4k - 18.2 MB)"
    url: "/assets/images/2019-06-09-jellyfish/downloads/jellyfish-full.jpg"
image: "https://user-images.githubusercontent.com/13140065/178388947-a59bbe42-bdf5-4b21-b1e8-0ccaef3cab1b.png"
default_image_fullwidth: true
featured: true
---

This is definitely my best render to date. I learned a ton
about modeling, C4D procedural deformers, and hair
simulation, and texturing.

# Modeling

The first phase was modeling. I followed Motion Viking's
[YouTube
tutorial](https://www.youtube.com/watch?v=11JwBQkzySE) to
model, rig, and animate a jellyfish in a procedural way.
_Procedural modeling_ differs from traditional modeling in
that each modification made to the base shape without
altering the original shape. This particular approach to
modeling allowed me to make changes to prior stages of the
work (like modeling the jellyfish bell) without having to
redo all subsequent steps.

## Hair!

This was the first project in which I modelled hair! It's
such a straightforward and valuable tool! Following Motion
Viking's tutorial, I added hair to the edge of the
jellyfish's bell and under where the tentacles grow from.
Finally, after adding some "hair-to-hair" forces and
lowering the effect of gravity to `-1 m/s/s` (to simulate
underwater effects), I had a realistic model for an
underwater jellyfish.

## Simulation

Motion Viking illustrated how to animate the motion of the
jellyfish on a spline, simluating how a real jellyfish may
move underwater. He went over detailed changes to the bell
deformation and "swoosh" actions of the jellyfish. The final
result of modeling:

<div class="embed-container-full-width">
<iframe src="https://www.youtube.com/embed/tcQxNEFJEjs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

After the simluation plays for roughly 300 frames, the
jellyfish moves into the middle of the spline with
realistic-looking hair. The final model appears as this in
Cinema 4D:

![](https://user-images.githubusercontent.com/13140065/178388942-32cf2853-46db-4fa8-a9d5-82c1efe4e467.png)

# Texturing

To create a realistic bioluminescent jellyfish, we want to
create some of the cool patterns found on real jellyfish. I
created this simple texture in Illustrator using mirroring
across the two axes.

![](https://user-images.githubusercontent.com/13140065/178388944-8d09f25a-d382-4dfe-bffc-5c9a2861b852.png)

Kinda looks like something from Avatar!

Next, following Motion Viking's tutorial, I animated the
texture in After Effects using displacement patterns and
luma mattes.

<div class="embed-container-full-width">
<iframe src="https://www.youtube.com/embed/f8ApFp-0CRo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

I applied this texture to the base model under the Emission
channel and added a camera bloom effect to emphasize the
glow of the jellyfish:

![](https://user-images.githubusercontent.com/13140065/178388945-66a01509-78ca-4a7a-8dec-f8c5b4c57c48.png)

# Final touches

I added an Octane Volume and created a rig to try and
simulate underwater light rays as would come through the
surface in real life. I also added some small green spheres
to look like little bioluminescent sea creatures:

![](https://user-images.githubusercontent.com/13140065/178388937-7948216c-c465-494e-81bf-71c593f9e484.png)
