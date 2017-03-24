#!python
from numpy import *
from numpy.random import *
try:
    from future_builtins import zip
except ImportError: # not 2.6+ or is 3.x
    try:
        from itertools import izip as zip # < 2.5 or 3.x
    except ImportError:
        pass





def resample(weights):
  n = len(weights)
  indices = [] # Find the discrete cumulative density function (CDF)

  C = [0.] + [sum(weights[:i+1]) for i in range(n)] # Select a random initial point

  u0, j = random(), 0
  for u in [(u0+i)/n for i in range(n)]: # U linearly grow to 1

    while u > C[j]: # Encounter small particles, skip
      j+=1
    indices.append(j-1) # Encounter big particles, add, u increase, there is the second time possible to be added
  return indices # Return the subscript of the big particle



def particlefilter(sequence, pos, stepsize, n):
#Sequence: represents the sequence of pictures
#Pos: the first frame of the target position
#Stepsize: the sampling range
# N: number of particles    
   seq = iter(sequence)
   x = ones((n, 2), int) * pos                   # Initial position
   f0 = seq.next()[tuple(pos)] * ones(n)         # Target colour model
   yield pos, x, ones(n)/n                       # Return expected position, particles and weights
   for im in seq:
      # Sprinkle around the particles in the previous frame as the particles of the current frame
      x += uniform(-stepsize, stepsize, x.shape)  # Particle motion model: uniform step 
      x  = x.clip(zeros(2), array(im.shape)-1).astype(int) # Clip out-of-bounds particles
      f  = im[tuple(x.T)]                         # Measure particle colours (# Get the pixel values for each particle)
      w  = 1./(1. + (f0-f)**2)                    # Weight~ inverse
#quadratic colour distance
# Find the difference from the target model, w is the weight vector corresponding to the particle one by one
# You can see the maximum weight of the pixel with a value of 255 (1.0)
      w /= sum(w)                                 # Normalize w
      yield sum(x.T*w, axis=1), x, w              # Return expected position, particles and weights
      if 1./sum(w**2) < n/2.:                     # If particle cloud degenerate:
        x=x[resample(w),:]                     # Resample particles according to weights
#!python
if __name__ == "__main__":
  from pylab import *
 
  import time
  ion() # Open the interactive mode
  seq = [ im for im in zeros((20,240,320), int)]      # Create an image sequence of 20 frames long
  x0 = array([120, 160])                              # Add a square with starting position x0 moving along trajectory xs
# The first frame of the center of the box coordinates
# Add a white box with a motion trajectory of xs for each image (the pixel value is 255, the x axis is added to each frame, and the vertical coordinate is added to 2)


  xs = vstack((arange(20)*3, arange(20)*2)).T + x0
  for t, x in enumerate(xs):
# T from 0, x from xs [0], enumerate function for traversing the elements in the sequence and their subscripts
# Slice of the use is also very interesting, it can be very convenient to use to access the array array seq subscript range
    xslice = slice(x[0]-8, x[0]+8)
    yslice = slice(x[1]-8, x[1]+8)
    seq[t][xslice, yslice] = 255

# Track white box through the sequence

  for im, p in zip(seq, particlefilter(seq, x0, 8, 100)): 
    pos, xs, ws = p
    position_overlay = zeros_like(im)
    position_overlay[tuple(pos)] = 1
    particle_overlay = zeros_like(im)
    particle_overlay[tuple(xs.T)] = 1
    hold(True)
    draw()
    time.sleep(0.3)
    clf()                                           # Causes flickering, but without the spy plots aren't overwritten
    imshow(im,cmap=cm.gray)                         # Plot the image
    spy(position_overlay, marker='.', color='b')    # Plot the expected position
    spy(particle_overlay, marker=',', color='r')    # Plot the particles
  show()

