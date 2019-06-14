---
layout: posts/post
author: Pramod Kotipalli
title:  Jellyfish
subtitle: Modeling, rigging, and animating a bioluminescent jellyfish
tags:
    - cinema-4d
    - octane-render
    - graphic-design
    - simulation
    - hair
    - adobe-illustrator
    - adobe-after-effects
downloads:
    - name: 📱 iPhone X (2436-by-1125 - 2.5 MB)
      url: /static/images/2019/06/09/jellyfish/downloads/jellyfish-iphone-x.jpg
    - name: 🖥️ Desktop (2560-by-1600 - 3.7 MB)
      url: /static/images/2019/06/09/jellyfish/downloads/jellyfish-desktop.jpg
    - name: 🖼️ Full (4096-by-4096, 4k - 18.2 MB)
      url: /static/images/2019/06/09/jellyfish/downloads/jellyfish-full.jpg
thumbnail_url: /static/images/2019/06/09/jellyfish/jellyfish-thumbnail.png
redirect_from: "/portfolio/jellyfish/"
default_image_fullwidth: True
---

![](/static/images/2019/06/09/jellyfish/jellyfish-thumbnail.png)

This is definitely my best render to date. I learned a ton about modeling, C4D procedural deformers, and hair simulation, and texturing.

# Modeling

The first phase was modeling. I followed Motion Viking's [YouTube tutorial](https://www.youtube.com/watch?v=11JwBQkzySE) to model, rig, and animate a jellyfish in a procedural way. _Procedural modeling_ differs from traditional modeling in that each modification made to the base shape without altering the original shape. This particular approach to modeling allowed me to make changes to prior stages of the work (like modeling the jellyfish bell) without having to redo all subsequent steps.

## Hair!

This was the first project in which I modelled hair! It's such a straightforward and valuable tool! Following Motion Viking's tutorial, I added hair to the edge of the jellyfish's bell and under where the tentacles grow from. Finally, after adding some "hair-to-hair" forces and lowering the effect of gravity to `-1 m/s/s` (to simulate underwater effects), I had a realistic model for an underwater jellyfish.

## Simulation

Motion Viking illustrated how to animate the motion of the jellyfish on a spline, simluating how a real jellyfish may move underwater. He went over detailed changes to the bell deformation and "swoosh" actions of the jellyfish. The final result of modeling:

<div class="embed-container-full-width">
<iframe src="https://www.youtube.com/embed/tcQxNEFJEjs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

After the simluation plays for roughly 300 frames, the jellyfish moves into the middle of the spline with realistic-looking hair. The final model appears as this in Cinema 4D:

![](/static/images/2019/06/09/jellyfish/jellyfish-model.png)

# Texturing

To create a realistic bioluminescent jellyfish, we want to create some of the cool patterns found on real jellyfish. I created this simple texture in Illustrator using mirroring across the two axes.

![](/static/images/2019/06/09/jellyfish/jellyfish-pattern.png)

Kinda looks like something from Avatar!

Next, following Motion Viking's tutorial, I animated the texture in After Effects using displacement patterns and luma mattes.

<div class="embed-container-full-width">
<iframe src="https://www.youtube.com/embed/f8ApFp-0CRo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

I applied this texture to the base model under the Emission channel and added a camera bloom effect to emphasize the glow of the jellyfish:

![](/static/images/2019/06/09/jellyfish/jellyfish-textured-simple.png)

# Final touches

I added an Octane Volume and created a rig to try and simulate underwater light rays as would come through the surface in real life. I also added some small green spheres to look like little bioluminescent sea creatures:


![](/static/images/2019/06/09/jellyfish/jellyfish-light-ray-rig-and-sealife.png)
