// ---------------------------------------
// Include the molecule
// ---------------------------------------
#include "edited_ala5.pov"


// ---------------------------------------
// Global settings
// ---------------------------------------
global_settings {
  assumed_gamma 1.0
}

#default {
  finish {
    ambient 0.05
    diffuse 0.9
    specular 0.0
    roughness 0.0
  }
  pigment {
    color rgb <1, 1, 1>
  }
}

background { color rgb <0.5, 0.5, 0.5> }


// ---------------------------------------
// Camera & lighting
// ---------------------------------------
camera {
  location <-10, 15, 0>
  look_at  <0, 0, 0>
  angle 50
}

light_source {
  <20, 30, -20>
  color rgb <0.3, 0.3, 0.3>
  shadowless
}

light_source {
  <-20, 20, -10>
  color rgb <0.3, 0.3, 0.3>
  shadowless
}

// ---------------------------------------
// Parameters
// ---------------------------------------
#declare N = 5;
#declare Radius = 6;

// ---------------------------------------
// Render molecule at pentagon vertices
// ---------------------------------------
#for (I, 0, N-1)
  #declare Angle = 2*pi*I/N;

  object {
    mol_0
    scale 0.5
    translate <Radius*cos(Angle), 0, Radius*sin(Angle)>
  }
#end
