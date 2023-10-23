# ChatGPT generated this font face

Prompt was something like this:

```
for c++ generate a 3d array for lower-case a-z characters as a mono font face. fill in this code:
static int[][][] mono = {
  // ...
};
only use 0s and 1s with a resolution of 8x8 for each character
```

```
@p13i ➜ /workspaces/cs (main) $ bazel run //cs/app/text:draw_to_console
INFO: Analyzed target //cs/app/text:draw_to_console (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //cs/app/text:draw_to_console up-to-date:
  bazel-bin/cs/app/text/draw_to_console
INFO: Elapsed time: 0.539s, Critical Path: 0.29s
INFO: 3 processes: 1 internal, 2 processwrapper-sandbox.
INFO: Build completed successfully, 3 total actions
INFO: Running command line: bazel-bin/cs/app/text/draw_to_console
a (index=0):
   oo
  o  o
 o    o
 oooooo
 o
 o



b (index=1):
 oo
 o o
 o  o
 o   o
 o   o
 o  o
 oo


c (index=2):
   ooo
  o   o
 o     o
 o     o
  o   o
   o o



d (index=3):
 oo
 o o
 o  o
 o   o
 o   o
 o  o
 oo


e (index=4):
 ooooo
 o
 o
 ooo
 o
 o
 ooooo


f (index=5):
 ooooo
 o
 o
 ooo
 o
 o
 o
 o

g (index=6):
   ooo
  o   o
 o     o
 o   oo
 o    o
  o
   o


h (index=7):
 o
 o
 o
 ooooo
 o    o
 o    o
 o    o
 o    o

i (index=8):
  ooo
    o



    o
  ooo


j (index=9):
   ooo
      o
       o
       o
       o
       o
  o   o
 o

k (index=10):
 o
 o
 o
 o   o
 o  o
 o o
 o  o
 o

l (index=11):
 o
 o
 o
 o
 o
 o



m (index=12):



 o oo o
 oo  oo
 o    o



n (index=13):



 o    o
 oo   o
 o o  o
 o  o o
 o   oo

o (index=14):
   oo
  o  o
 o    o
 o    o
 o    o
 o    o
  o  o
   oo

p (index=15):







 ooo

q (index=16):






 o
    ooo

r (index=17):




 o
 oo
 o o
 o  o

s (index=18):
   ooo
  o   o
 o
  o   o
   ooo
      o
       o
 ooooo

t (index=19):
 ooo
   o
   o
   o
   o
   o
   o


u (index=20):
 o
 o
 o
 o
 o
 o
  o


v (index=21):
 o
 o
 o
 o
 o
  o
   o


w (index=22):
 o
 o
 o
 o
 oo   o
   o
   o


x (index=23):
 o
 o
 o
  o
   o
    o
  o
 o

y (index=24):
 o
 o
 o
 o
 o
  o
   o


z (index=25):
 oooooo
      o
     o
    o
   o
  o
 o
 oooooo

@p13i ➜ /workspaces/cs (main) $
```
