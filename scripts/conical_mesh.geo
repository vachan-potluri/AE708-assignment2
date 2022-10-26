/*
Point numbering convention:
    0xx: nozzle contour (converging and diverging), except parabolic profile
    1xx: temporary points
    2xx: parabolic profile spline
Line numbering convention:
    0xx: nozzle contours, including parabolic profile spline
Curve loops, surface convention:
    0xx: all
*/

R_t = 1; // throat radius
theta_conical = 15*Pi/180; // half cone angle
theta_n = theta_conical;
theta_i = 75*Pi/180; // angle at inlet section
epsilon = 4; // exit area to throat area ratio
R_e = R_t*Sqrt(epsilon); // exit radius
Rc_div = 0.4*R_t; // radius of curvature just after throat in diverging section
Rc_conv = 1.5*R_t; // radius of curvature of converging section

x_n = Rc_div*Sin(theta_n); // coordinates of point N
y_n = R_t + Rc_div*(1-Cos(theta_n));
x_i = -Rc_conv*Sin(theta_i); // coordinates of inlet section
y_i = R_t + Rc_conv*(1-Cos(theta_i));
x_e = x_n + (R_e-y_n)/Tan(theta_conical); // x coordinate of exit section
revolution_angle = 3*Pi/180; // body's revolution angle

// converging section (circular arc)
Point(100) = {0, R_t+Rc_conv, 0}; // arc center
Point(1) = {x_i, y_i, 0};
Point(2) = {0, R_t, 0};
Point(3) = {x_i, 0, 0};
Point(4) = {0, 0, 0};
Circle(1) = {1, 100, 2};
Line(2) = {3,4};
Line(3) = {3,1};
Line(4) = {4,2};
Curve Loop(1) = {2,4,-1,-3};

// circular arc after throat
Point(101) = {0, R_t+Rc_div, 0}; // arc center
Point(5) = {x_n, y_n, 0};
Point(6) = {x_n, 0, 0};
Circle(5) = {2, 101, 5};
Line(6) = {4,6};
Line(7) = {6,5};
Curve Loop(2) = {6,7,-5,-4};

// conical portion
/// define points on the parabolic section
Point(7) = {x_e, R_e, 0};
Point(8) = {x_e, 0, 0};
Line(8) = {5,7};
Line(9) = {6,8};
Line(10) = {8,7};
Curve Loop(3) = {9,10,-8,-7};



// plane surfaces, transfinite and recombine; extrude and physical entities
Transfinite Curve{1} = 41 Using Bump 0.1;
Transfinite Curve{2} = 41 Using Bump 0.15;
Transfinite Curve{5,6} = 11;
Transfinite Curve{8,9} = 41 Using Progression 1.1;
Transfinite Curve{3,4,7,10} = 31;
For i In {1:3}
    Plane Surface(i) = {i};
    Transfinite Surface{i};
    Recombine Surface{i};
    out~{i}[] = Extrude{
        {1,0,0},
        {0,0,0},
        revolution_angle
    }{
        Surface{i};
        Layers{1};
        Recombine;
    };
EndFor
// rotate all entities for symmetry about xy plane
Rotate{
    {1,0,0},
    {0,0,0},
    -0.5*revolution_angle
}{
    Point{:}; Curve{:}; Surface{:}; Volume{:};
}
Physical Volume("volume", 1) = {};
Physical Surface("back", 1) = {};
Physical Surface("front", 2) = {};
Physical Surface("inflow", 3) = {};
Physical Surface("outflow", 4) = {};
Physical Surface("wall", 5) = {};
For i In {1:3}
    Physical Volume(1) += {out~{i}[1]};
    Physical Surface(1) += {i};
    Physical Surface(2) += {out~{i}[0]};
    Physical Surface(5) += {out~{i}[3]};
EndFor
Physical Surface(3) += {out_1[4]};
Physical Surface(4) += {out_3[2]};

Mesh 3;

